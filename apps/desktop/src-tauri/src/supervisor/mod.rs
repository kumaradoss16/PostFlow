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
    child_handle: Arc<Mutex<Option<tokio::process::Child>>>,
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
            child_handle: Arc::new(Mutex::new(None)),
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
            const CREATE_NO_WINDOW: u32 = 0x08000000;

            let mut cmd = tokio::process::Command::new(&python_exe);
            cmd.args(["-m", "postflow.main", "--bootstrap-pipe", &pipe_name]);
            if backend_dir.exists() {
                cmd.current_dir(&backend_dir);
            }
            cmd.env("PYTHONUNBUFFERED", "1");
            cmd.creation_flags(CREATE_NO_WINDOW);

            let child = match cmd.spawn() {
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
                    return Err(err);
                }
            };

            *self.child_pid.write().await = Some(pid);
            *self.child_handle.lock().await = Some(child);
            *self.state.write().await = SupervisorState::Authenticating;

            // Wait for handshake with 30s timeout
            let handshake_res = tokio::time::timeout(
                Duration::from_secs(30),
                bootstrap::run_windows_pipe_handshake(&pipe_name, pid),
            )
            .await;

            match handshake_res {
                Ok(Ok((port, auth_token))) => {
                    *self.port.write().await = Some(port);
                    *self.auth_token.write().await = Some(auth_token);
                    *self.started_at.write().await = Some(Instant::now());
                    *self.state.write().await = SupervisorState::Ready;
                    Ok(self.get_status().await)
                }
                Ok(Err(e)) => {
                    let err = format!("Backend bootstrap handshake failed: {}", e);
                    *self.last_error.write().await = Some(err.clone());
                    *self.state.write().await = SupervisorState::Failed;
                    let _ = self.stop().await;
                    Err(err)
                }
                Err(_) => {
                    let err = "Backend bootstrap timed out after 30 seconds".to_string();
                    *self.last_error.write().await = Some(err.clone());
                    *self.state.write().await = SupervisorState::Failed;
                    let _ = self.stop().await;
                    Err(err)
                }
            }
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

        // 1. Send graceful shutdown request if port and auth token exist
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

        // 2. Wait up to 5s for child process to exit cleanly, then kill
        let mut child_guard = self.child_handle.lock().await;
        if let Some(mut child) = child_guard.take() {
            let wait_res = tokio::time::timeout(Duration::from_secs(5), child.wait()).await;
            match wait_res {
                Ok(Ok(exit_status)) => {
                    log_or_print(&format!("Backend child exited cleanly: {}", exit_status));
                }
                _ => {
                    let _ = child.kill().await;
                    let _ = child.wait().await;
                }
            }
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

fn log_or_print(_msg: &str) {}

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
}
