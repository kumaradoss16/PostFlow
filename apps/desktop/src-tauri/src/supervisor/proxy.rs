use serde::{Deserialize, Serialize};
use std::collections::HashMap;

const MAX_REQUEST_BODY_BYTES: usize = 1024 * 1024; // 1 MB
const MAX_RESPONSE_BODY_BYTES: usize = 5 * 1024 * 1024; // 5 MB
const AUTH_HEADER_NAME: &str = "X-PostFlow-Local-Auth";

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct BackendProxyRequest {
    pub method: String,
    pub path: String,
    pub query: Option<HashMap<String, String>>,
    pub body: Option<serde_json::Value>,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "camelCase")]
pub struct BackendProxyResponse {
    pub status_code: u16,
    pub data: Option<serde_json::Value>,
    pub error: Option<String>,
}

pub fn validate_proxy_request(req: &BackendProxyRequest) -> Result<(), String> {
    // 1. Validate HTTP method
    let method = req.method.to_uppercase();
    match method.as_str() {
        "GET" | "POST" | "PUT" | "DELETE" | "PATCH" => {}
        _ => return Err(format!("Disallowed HTTP method: {}", req.method)),
    }

    // 2. Validate path allowlist: strictly /api/v1/*
    if !req.path.starts_with("/api/v1/") {
        return Err(format!(
            "Access denied: path '{}' must start with '/api/v1/'",
            req.path
        ));
    }

    // 3. Prevent path traversal and suspicious patterns
    if req.path.contains("..") || req.path.contains("//") || req.path.contains('\\') {
        return Err("Access denied: path contains traversal or invalid characters".to_string());
    }

    // 4. Request size check if body is present
    if let Some(ref body) = req.body {
        let serialized = serde_json::to_string(body).map_err(|e| e.to_string())?;
        if serialized.len() > MAX_REQUEST_BODY_BYTES {
            return Err(format!(
                "Request body exceeds maximum allowed size of {} bytes",
                MAX_REQUEST_BODY_BYTES
            ));
        }
    }

    Ok(())
}

pub async fn execute_proxy_request(
    client: &reqwest::Client,
    port: u16,
    auth_token: &str,
    req: &BackendProxyRequest,
) -> Result<BackendProxyResponse, String> {
    validate_proxy_request(req)?;

    let url = format!("http://127.0.0.1:{}{}", port, req.path);

    let method = match req.method.to_uppercase().as_str() {
        "GET" => reqwest::Method::GET,
        "POST" => reqwest::Method::POST,
        "PUT" => reqwest::Method::PUT,
        "DELETE" => reqwest::Method::DELETE,
        "PATCH" => reqwest::Method::PATCH,
        _ => return Err("Invalid method".to_string()),
    };

    let mut request_builder = client
        .request(method, &url)
        .header(AUTH_HEADER_NAME, auth_token)
        .header(reqwest::header::HOST, "127.0.0.1");

    if let Some(ref query) = req.query {
        request_builder = request_builder.query(query);
    }

    if let Some(ref body) = req.body {
        request_builder = request_builder.json(body);
    }

    let response = request_builder
        .send()
        .await
        .map_err(|e| format!("Proxy HTTP request failed: {}", e))?;

    let status_code = response.status().as_u16();

    // Check Content-Length before downloading if present
    if let Some(len) = response.content_length() {
        if len as usize > MAX_RESPONSE_BODY_BYTES {
            return Err(format!(
                "Backend response size exceeds maximum allowed limit of {} bytes",
                MAX_RESPONSE_BODY_BYTES
            ));
        }
    }

    let body_bytes = response
        .bytes()
        .await
        .map_err(|e| format!("Failed to read backend response body: {}", e))?;

    if body_bytes.len() > MAX_RESPONSE_BODY_BYTES {
        return Err(format!(
            "Backend response body exceeded maximum limit of {} bytes",
            MAX_RESPONSE_BODY_BYTES
        ));
    }

    let (data, error) = if body_bytes.is_empty() {
        (None, None)
    } else {
        match serde_json::from_slice::<serde_json::Value>(&body_bytes) {
            Ok(json) => {
                if status_code >= 400 {
                    let err_msg = json
                        .get("detail")
                        .or_else(|| json.get("error"))
                        .and_then(|v| v.as_str())
                        .unwrap_or("HTTP error response")
                        .to_string();
                    (Some(json), Some(err_msg))
                } else {
                    (Some(json), None)
                }
            }
            Err(_) => {
                let text = String::from_utf8_lossy(&body_bytes).to_string();
                if status_code >= 400 {
                    (None, Some(text))
                } else {
                    (Some(serde_json::Value::String(text)), None)
                }
            }
        }
    };

    Ok(BackendProxyResponse {
        status_code,
        data,
        error,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_validate_allowed_route() {
        let req = BackendProxyRequest {
            method: "GET".to_string(),
            path: "/api/v1/health".to_string(),
            query: None,
            body: None,
        };
        assert!(validate_proxy_request(&req).is_ok());
    }

    #[test]
    fn test_reject_unallowed_prefix() {
        let req = BackendProxyRequest {
            method: "GET".to_string(),
            path: "/health".to_string(),
            query: None,
            body: None,
        };
        let err = validate_proxy_request(&req).unwrap_err();
        assert!(err.contains("must start with '/api/v1/'"));
    }

    #[test]
    fn test_reject_path_traversal() {
        let req = BackendProxyRequest {
            method: "GET".to_string(),
            path: "/api/v1/../../etc/passwd".to_string(),
            query: None,
            body: None,
        };
        let err = validate_proxy_request(&req).unwrap_err();
        assert!(err.contains("traversal"));
    }

    #[test]
    fn test_reject_disallowed_method() {
        let req = BackendProxyRequest {
            method: "CONNECT".to_string(),
            path: "/api/v1/test".to_string(),
            query: None,
            body: None,
        };
        let err = validate_proxy_request(&req).unwrap_err();
        assert!(err.contains("Disallowed HTTP method"));
    }
}
