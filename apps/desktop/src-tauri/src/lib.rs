pub mod supervisor;

use serde::{Deserialize, Serialize};
use std::sync::Arc;
use supervisor::{BackendProxyRequest, BackendProxyResponse, Supervisor, SupervisorStatus};
use tauri::State;

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct AppInfoResponse {
    pub name: String,
    pub version: String,
    pub tauri_version: String,
    pub rust_version: Option<String>,
    pub platform: String,
    pub arch: String,
}

#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct BackendHealthResponse {
    pub status: String,
    pub version: String,
    pub environment: String,
    pub host: String,
}

pub struct AppState {
    pub supervisor: Arc<Supervisor>,
}

/// Retrieve desktop application identity and platform metadata.
#[tauri::command]
fn get_app_info() -> Result<AppInfoResponse, String> {
    Ok(AppInfoResponse {
        name: "PostFlow".to_string(),
        version: env!("CARGO_PKG_VERSION").to_string(),
        tauri_version: tauri::VERSION.to_string(),
        rust_version: Some(rustc_version_runtime()),
        platform: std::env::consts::OS.to_string(),
        arch: std::env::consts::ARCH.to_string(),
    })
}

/// Retrieve current backend supervisor lifecycle state.
#[tauri::command]
async fn backend_get_status(state: State<'_, AppState>) -> Result<SupervisorStatus, String> {
    Ok(state.supervisor.get_status().await)
}

/// Start the backend process and perform secure bootstrap handshake.
#[tauri::command]
async fn backend_start(state: State<'_, AppState>) -> Result<SupervisorStatus, String> {
    state.supervisor.start().await
}

/// Stop the backend process gracefully.
#[tauri::command]
async fn backend_stop(state: State<'_, AppState>) -> Result<SupervisorStatus, String> {
    state.supervisor.stop().await
}

/// Mediate HTTP request to local backend through secure Rust proxy.
#[tauri::command]
async fn backend_proxy_request(
    state: State<'_, AppState>,
    request: BackendProxyRequest,
) -> Result<BackendProxyResponse, String> {
    state.supervisor.proxy_request(request).await
}

/// Health check command proxying to /api/v1/health.
#[tauri::command]
async fn check_backend_health(state: State<'_, AppState>) -> Result<BackendHealthResponse, String> {
    let proxy_req = BackendProxyRequest {
        method: "GET".to_string(),
        path: "/api/v1/health".to_string(),
        query: None,
        body: None,
    };

    let proxy_res = state.supervisor.proxy_request(proxy_req).await?;

    if let Some(data) = proxy_res.data {
        serde_json::from_value::<BackendHealthResponse>(data)
            .map_err(|e| format!("Failed to parse health response: {}", e))
    } else {
        Err(proxy_res
            .error
            .unwrap_or_else(|| "Unknown backend health error".to_string()))
    }
}

fn rustc_version_runtime() -> String {
    format!("{}-{}", std::env::consts::OS, std::env::consts::ARCH)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    let supervisor = Arc::new(Supervisor::new(None));
    let supervisor_exit = supervisor.clone();

    let app = tauri::Builder::default()
        .manage(AppState { supervisor })
        .invoke_handler(tauri::generate_handler![
            get_app_info,
            backend_get_status,
            backend_start,
            backend_stop,
            backend_proxy_request,
            check_backend_health,
        ])
        .build(tauri::generate_context!())
        .expect("error while building PostFlow desktop application");

    app.run(move |_app_handle, event| {
        if let tauri::RunEvent::ExitRequested { .. } | tauri::RunEvent::Exit = event {
            let sup = supervisor_exit.clone();
            let _ = tokio::runtime::Runtime::new().map(|rt| {
                rt.block_on(sup.stop());
            });
        }
    });
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_get_app_info() {
        let info = get_app_info().expect("get_app_info failed");
        assert_eq!(info.name, "PostFlow");
        assert_eq!(info.version, "0.1.0");
        assert!(!info.tauri_version.is_empty());
    }
}
