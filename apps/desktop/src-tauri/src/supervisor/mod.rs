pub mod bootstrap;
pub mod proxy;

use serde::{Deserialize, Serialize};
use std::path::{Path, PathBuf};
use std::sync::Arc;
use std::time::{Duration, Instant};
use tokio::sync::{Mutex, RwLock};

pub use bootstrap::{BootstrapAck, BootstrapAuthorize, BootstrapInit, BootstrapReady};
pub use proxy::{BackendProxyRequest, BackendProxyResponse};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum SupervisorState {
    Stopped,
    Starting,
    Authenticating,
    Ready,
    Degraded,
    Stopping,
    Failed,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct SupervisorStatus {
    pub state: SupervisorState,
    pub port: Option<u16>,
    pub pid: Option<u32>,
    pub uptime_seconds: Option<u64>,
    pub last_error: Option<String>,
}

#[derive(Clone)]
pub struct Supervisor {
    state: Arc<RwLock<SupervisorState>>,
    port: Arc<RwLock<Option<u16>>>,
    auth_token: Arc<RwLock<Option<String>>>,
    child_pid: Arc<RwLock<Option<u32>>>,
    started_at: Arc<RwLock<Option<Instant>>>,
    last_error: Arc<RwLock<Option<String>>>,
    shutdown_trigger: Arc<Mutex<Option<tokio::sync::oneshot::Sender<()>>>>,
    monitor_done: Arc<Mutex<Option<tokio::sync::oneshot::Receiver<()>>>>,
    http_client: reqwest::Client,
    explicit_python_path: Option<PathBuf>,
}

impl Supervisor {
    pub fn new(explicit_python_path: Option<PathBuf>) -> Self {
        Self {
            state: Arc::new(RwLock::new(SupervisorState::Stopped)),
            port: Arc::new(RwLock::new(None)),
            auth_token: Arc::new(RwLock::new(None)),
            child_pid: Arc::new(RwLock::new(None)),
            started_at: Arc::new(RwLock::new(None)),
            last_error: Arc::new(RwLock::new(None)),
            shutdown_trigger: Arc::new(Mutex::new(None)),
            monitor_done: Arc::new(Mutex::new(None)),
            http_client: reqwest::Client::builder()
                .timeout(Duration::from_secs(10))
                .build()
                .unwrap_or_default(),
            explicit_python_path,
        }
    }

    pub async fn get_status(&self) -> SupervisorStatus {
        let state = *self.state.read().await;
        let port = *self.port.read().await;
        let pid = *self.child_pid.read().await;
        let uptime = self
            .started_at
            .read()
            .await
            .as_ref()
            .map(|t| t.elapsed().as_secs());
        let last_error = self.last_error.read().await.clone();

        SupervisorStatus {
            state,
            port,
            pid,
            uptime_seconds: uptime,
            last_error,
        }
    }

    pub fn resolve_python_path(&self) -> (PathBuf, PathBuf) {
        if let Some(ref path) = self.explicit_python_path {
            if path.exists() {
                let backend_dir = path
                    .parent()
                    .and_then(|p| p.parent())
                    .map(|p| p.to_path_buf())
                    .unwrap_or_else(|| PathBuf::from("."));
                return (path.clone(), backend_dir);
            }
        }

        // Try environment variable override
        if let Ok(env_path) = std::env::var("POSTFLOW_PYTHON_PATH") {
            let p = PathBuf::from(env_path);
            if p.exists() {
                let backend_dir = p
                    .parent()
                    .and_then(|par| par.parent())
                    .map(|par| par.to_path_buf())
                    .unwrap_or_else(|| PathBuf::from("."));
                return (p, backend_dir);
            }
        }

        // Check standard relative locations from workspace root
        let candidates = [
            // From root
            ("apps/backend/.venv/Scripts/python.exe", "apps/backend"),
            ("apps/backend/.venv/bin/python", "apps/backend"),
            // From apps/desktop/src-tauri
            (
                "../../../apps/backend/.venv/Scripts/python.exe",
                "../../../apps/backend",
            ),
            (
                "../../../apps/backend/.venv/bin/python",
                "../../../apps/backend",
            ),
            // Sibling
            ("../backend/.venv/Scripts/python.exe", "../backend"),
            ("../backend/.venv/bin/python", "../backend"),
        ];

        for (py, b_dir) in candidates {
            let py_buf = PathBuf::from(py);
            if py_buf.exists() {
                return (py_buf, PathBuf::from(b_dir));
            }
        }

        // Fallback to system python
        let sys_python = if cfg!(windows) {
            "python.exe"
        } else {
            "python3"
        };
        (PathBuf::from(sys_python), PathBuf::from("apps/backend"))
    }

    pub async fn start(&self) -> Result<SupervisorStatus, String> {
        let current_state = *self.state.read().await;
        if current_state == SupervisorState::Ready {
            return Ok(self.get_status().await);
        }
        if current_state == SupervisorState::Starting
            || current_state == SupervisorState::Authenticating
        {
            return Err("Supervisor is already in the process of starting".to_string());
        }

        *self.state.write().await = SupervisorState::Starting;
        *self.last_error.write().await = None;

        let (python_exe, backend_dir) = self.resolve_python_path();
        let pipe_name = bootstrap::generate_pipe_name();

        #[cfg(windows)]
        {
            // F3: Pre-create named pipe server BEFORE spawning the child process
            let pipe_server = match bootstrap::create_windows_pipe_server(&pipe_name) {
                Ok(s) => s,
                Err(e) => {
                    let err = format!("Failed to pre-create bootstrap named pipe: {}", e);
                    *self.last_error.write().await = Some(err.clone());
                    *self.state.write().await = SupervisorState::Failed;
                    return Err(err);
                }
            };

            const CREATE_NO_WINDOW: u32 = 0x08000000;

            let mut cmd = tokio::process::Command::new(&python_exe);
            cmd.args(["-m", "postflow.main", "--bootstrap-pipe", &pipe_name]);
            if backend_dir.exists() {
                cmd.current_dir(&backend_dir);
            }
            cmd.env("PYTHONUNBUFFERED", "1");
            cmd.creation_flags(CREATE_NO_WINDOW);

            let mut child = match cmd.spawn() {
                Ok(c) => c,
                Err(e) => {
                    let err = format!(
                        "Failed to spawn backend child process (python: '{}', dir: '{}'): {}",
                        python_exe.display(),
                        backend_dir.display(),
                        e
                    );
                    *self.last_error.write().await = Some(err.clone());
                    *self.state.write().await = SupervisorState::Failed;
                    return Err(err);
                }
            };

            let pid = match child.id() {
                Some(id) => id,
                None => {
                    let err = "Failed to obtain child process ID".to_string();
                    *self.last_error.write().await = Some(err.clone());
                    *self.state.write().await = SupervisorState::Failed;
                    let _ = child.kill().await;
                    return Err(err);
                }
            };

            *self.child_pid.write().await = Some(pid);
            *self.state.write().await = SupervisorState::Authenticating;

            // Wait for handshake with 30s timeout on pre-created pipe server
            let handshake_res = tokio::time::timeout(
                Duration::from_secs(30),
                bootstrap::complete_windows_pipe_handshake(pipe_server, pid),
            )
            .await;

            let (port, auth_token) = match handshake_res {
                Ok(Ok((p, tok))) => (p, tok),
                Ok(Err(e)) => {
                    let err = format!("Backend bootstrap handshake failed: {}", e);
                    *self.last_error.write().await = Some(err.clone());
                    *self.state.write().await = SupervisorState::Failed;
                    let _ = child.kill().await;
                    let _ = child.wait().await;
                    *self.child_pid.write().await = None;
                    return Err(err);
                }
                Err(_) => {
                    let err = "Backend bootstrap timed out after 30 seconds".to_string();
                    *self.last_error.write().await = Some(err.clone());
                    *self.state.write().await = SupervisorState::Failed;
                    let _ = child.kill().await;
                    let _ = child.wait().await;
                    *self.child_pid.write().await = None;
                    return Err(err);
                }
            };

            *self.port.write().await = Some(port);
            *self.auth_token.write().await = Some(auth_token);
            *self.started_at.write().await = Some(Instant::now());
            *self.state.write().await = SupervisorState::Ready;

            // F4: Spawn process monitor task watching the child process
            let (shutdown_tx, shutdown_rx) = tokio::sync::oneshot::channel::<()>();
            let (done_tx, done_rx) = tokio::sync::oneshot::channel::<()>();

            let state_clone = self.state.clone();
            let port_clone = self.port.clone();
            let auth_token_clone = self.auth_token.clone();
            let child_pid_clone = self.child_pid.clone();
            let started_at_clone = self.started_at.clone();
            let last_error_clone = self.last_error.clone();

            tokio::spawn(async move {
                tokio::select! {
                    exit_res = child.wait() => {
                        let mut state = state_clone.write().await;
                        // Only mark Failed if not in deliberate stopping/stopped state
                        if *state != SupervisorState::Stopping && *state != SupervisorState::Stopped {
                            let err = match exit_res {
                                Ok(status) => format!("Backend child process terminated unexpectedly ({})", status),
                                Err(e) => format!("Failed waiting on backend child: {}", e),
                            };
                            *last_error_clone.write().await = Some(err);
                            *state = SupervisorState::Failed;
                            *port_clone.write().await = None;
                            *auth_token_clone.write().await = None;
                            *child_pid_clone.write().await = None;
                            *started_at_clone.write().await = None;
                        }
                        let _ = done_tx.send(());
                    }
                    _ = shutdown_rx => {
                        // Intentional shutdown requested: allow up to 5s for child to exit cleanly
                        let wait_res = tokio::time::timeout(Duration::from_secs(5), child.wait()).await;
                        if wait_res.is_err() {
                            // Timeout expired: forced termination fallback
                            let _ = child.kill().await;
                            let _ = child.wait().await;
                        }
                        let _ = done_tx.send(());
                    }
                }
            });

            *self.shutdown_trigger.lock().await = Some(shutdown_tx);
            *self.monitor_done.lock().await = Some(done_rx);

            Ok(self.get_status().await)
        }

        #[cfg(not(windows))]
        {
            let err = "Supervisor requires Windows Named Pipes for secure bootstrap".to_string();
            *self.last_error.write().await = Some(err.clone());
            *self.state.write().await = SupervisorState::Failed;
            Err(err)
        }
    }

    pub async fn stop(&self) -> Result<SupervisorStatus, String> {
        let current_state = *self.state.read().await;
        if current_state == SupervisorState::Stopped {
            return Ok(self.get_status().await);
        }

        *self.state.write().await = SupervisorState::Stopping;

        // 1. Send authenticated graceful shutdown request to FastAPI
        let port_opt = *self.port.read().await;
        let token_opt = self.auth_token.read().await.clone();

        if let (Some(port), Some(token)) = (port_opt, token_opt) {
            let shutdown_url = format!("http://127.0.0.1:{}/api/v1/shutdown", port);
            let _ = self
                .http_client
                .post(&shutdown_url)
                .header("X-PostFlow-Local-Auth", token)
                .timeout(Duration::from_secs(2))
                .send()
                .await;
        }

        // 2. Trigger monitor task shutdown and wait for process completion
        let trigger = self.shutdown_trigger.lock().await.take();
        if let Some(tx) = trigger {
            let _ = tx.send(());
        }

        let done_rx = self.monitor_done.lock().await.take();
        if let Some(rx) = done_rx {
            // Allow up to 6 seconds for monitor task to complete clean exit or forced fallback
            let _ = tokio::time::timeout(Duration::from_secs(6), rx).await;
        }

        // 3. Clear state
        *self.port.write().await = None;
        *self.auth_token.write().await = None;
        *self.child_pid.write().await = None;
        *self.started_at.write().await = None;
        *self.state.write().await = SupervisorState::Stopped;

        Ok(self.get_status().await)
    }

    pub async fn proxy_request(
        &self,
        req: BackendProxyRequest,
    ) -> Result<BackendProxyResponse, String> {
        let state = *self.state.read().await;
        if state != SupervisorState::Ready {
            return Err(format!("Backend is not ready (current state: {:?})", state));
        }

        let port = self
            .port
            .read()
            .await
            .ok_or("Backend listener port is not configured")?;
        let token = self
            .auth_token
            .read()
            .await
            .clone()
            .ok_or("Backend authorization token is not set")?;

        proxy::execute_proxy_request(&self.http_client, port, &token, &req).await
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_supervisor_initial_state() {
        let supervisor = Supervisor::new(None);
        let status = tokio::runtime::Runtime::new()
            .unwrap()
            .block_on(supervisor.get_status());
        assert_eq!(status.state, SupervisorState::Stopped);
        assert!(status.port.is_none());
        assert!(status.pid.is_none());
    }

    #[tokio::test]
    async fn test_proxy_request_rejects_when_not_ready() {
        let supervisor = Supervisor::new(None);
        let req = BackendProxyRequest {
            method: "GET".to_string(),
            path: "/api/v1/health".to_string(),
            query: None,
            body: None,
        };
        let res = supervisor.proxy_request(req).await;
        assert!(res.is_err());
        assert!(res.unwrap_err().contains("Backend is not ready"));
    }

    #[tokio::test]
    async fn test_supervisor_stop_idempotent() {
        let supervisor = Supervisor::new(None);
        let res1 = supervisor.stop().await.expect("First stop failed");
        assert_eq!(res1.state, SupervisorState::Stopped);

        let res2 = supervisor.stop().await.expect("Second stop failed");
        assert_eq!(res2.state, SupervisorState::Stopped);
    }

    #[tokio::test]
    async fn test_proxy_request_rejects_when_failed() {
        let supervisor = Supervisor::new(None);
        *supervisor.state.write().await = SupervisorState::Failed;
        *supervisor.last_error.write().await = Some("Child terminated unexpectedly".to_string());

        let req = BackendProxyRequest {
            method: "GET".to_string(),
            path: "/api/v1/health".to_string(),
            query: None,
            body: None,
        };
        let res = supervisor.proxy_request(req).await;
        assert!(res.is_err());
        assert!(res.unwrap_err().contains("Backend is not ready"));
    }

    #[tokio::test]
    async fn test_supervisor_concurrency_start_guard() {
        let supervisor = Supervisor::new(None);
        *supervisor.state.write().await = SupervisorState::Starting;

        let res = supervisor.start().await;
        assert!(res.is_err());
        assert!(res
            .unwrap_err()
            .contains("already in the process of starting"));
    }
}
