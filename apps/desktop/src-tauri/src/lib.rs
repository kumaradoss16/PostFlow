use serde::{Deserialize, Serialize};

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

/// Retrieve desktop application identity and platform metadata.
#[tauri::command]
pub fn get_app_info() -> Result<AppInfoResponse, String> {
    Ok(AppInfoResponse {
        name: "PostFlow".to_string(),
        version: env!("CARGO_PKG_VERSION").to_string(),
        tauri_version: tauri::VERSION.to_string(),
        rust_version: Some(rustc_version_runtime()),
        platform: std::env::consts::OS.to_string(),
        arch: std::env::consts::ARCH.to_string(),
    })
}

/// Development verification command for backend health.
/// NOTE: In M1.2, this is replaced by the supervised child process
/// lifecycle and protected bootstrap pipe handshake.
#[tauri::command]
pub fn check_backend_health() -> Result<BackendHealthResponse, String> {
    Ok(BackendHealthResponse {
        status: "ok".to_string(),
        version: "0.1.0".to_string(),
        environment: "development".to_string(),
        host: "127.0.0.1".to_string(),
    })
}

fn rustc_version_runtime() -> String {
    format!("{}-{}", std::env::consts::OS, std::env::consts::ARCH)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![get_app_info, check_backend_health])
        .run(tauri::generate_context!())
        .expect("error while running PostFlow desktop application");
}

#[cfg(test)]
mod tests {
    use super::{check_backend_health, get_app_info};

    #[test]
    fn test_get_app_info() {
        let info = get_app_info().expect("get_app_info failed");
        assert_eq!(info.name, "PostFlow");
        assert_eq!(info.version, "0.1.0");
        assert!(!info.tauri_version.is_empty());
    }

    #[test]
    fn test_check_backend_health() {
        let health = check_backend_health().expect("check_backend_health failed");
        assert_eq!(health.status, "ok");
        assert_eq!(health.host, "127.0.0.1");
    }
}
