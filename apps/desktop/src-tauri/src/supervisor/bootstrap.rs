use rand::RngCore;
use serde::{Deserialize, Serialize};
use std::fmt::Write as _;
use subtle::ConstantTimeEq;
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};

pub const PROTOCOL_VERSION: u32 = 1;

#[derive(Debug, Serialize, Deserialize, PartialEq, Eq)]
pub struct BootstrapInit {
    pub protocol_version: u32,
    pub challenge_nonce: String,
}

#[derive(Debug, Serialize, Deserialize, PartialEq, Eq)]
pub struct BootstrapReady {
    pub echoed_challenge: String,
    pub port: u16,
    pub backend_nonce: String,
}

#[derive(Debug, Serialize, Deserialize, PartialEq, Eq)]
pub struct BootstrapAuthorize {
    pub auth_token: String,
    pub backend_nonce_ack: String,
}

#[derive(Debug, Serialize, Deserialize, PartialEq, Eq)]
pub struct BootstrapAck {
    pub status: String,
}

pub fn generate_random_hex(bytes: usize) -> String {
    let mut data = vec![0u8; bytes];
    rand::thread_rng().fill_bytes(&mut data);
    let mut hex = String::with_capacity(bytes * 2);
    for b in data {
        let _ = write!(hex, "{:02x}", b);
    }
    hex
}

pub fn generate_pipe_name() -> String {
    let id = uuid::Uuid::new_v4();
    format!(r"\\.\pipe\postflow-bootstrap-{}", id)
}

/// Perform protocol handshake over any bidirectional async stream (used for both Windows named pipe and testing).
pub async fn perform_handshake_over_stream<R, W>(
    reader: R,
    mut writer: W,
) -> Result<(u16, String), String>
where
    R: tokio::io::AsyncRead + Unpin,
    W: tokio::io::AsyncWrite + Unpin,
{
    let mut lines = BufReader::new(reader).lines();

    // Step 1: Send BootstrapInit
    let challenge_nonce = generate_random_hex(32);
    let init_msg = BootstrapInit {
        protocol_version: PROTOCOL_VERSION,
        challenge_nonce: challenge_nonce.clone(),
    };
    let mut init_json = serde_json::to_string(&init_msg).map_err(|e| e.to_string())?;
    init_json.push('\n');
    writer
        .write_all(init_json.as_bytes())
        .await
        .map_err(|e| format!("Failed to send BootstrapInit: {}", e))?;
    writer
        .flush()
        .await
        .map_err(|e| format!("Failed to flush BootstrapInit: {}", e))?;

    // Step 2: Read BootstrapReady
    let ready_line = lines
        .next_line()
        .await
        .map_err(|e| format!("Failed to read BootstrapReady line: {}", e))?
        .ok_or_else(|| "Connection closed by backend before BootstrapReady".to_string())?;

    let ready_msg: BootstrapReady = serde_json::from_str(&ready_line)
        .map_err(|e| format!("Invalid BootstrapReady payload: {}: {}", e, ready_line))?;

    if ready_msg.port == 0 {
        return Err("Backend reported invalid port 0".to_string());
    }

    // Validate echoed challenge in constant time
    let echoed_bytes = ready_msg.echoed_challenge.as_bytes();
    let challenge_bytes = challenge_nonce.as_bytes();
    if echoed_bytes.len() != challenge_bytes.len()
        || echoed_bytes.ct_eq(challenge_bytes).unwrap_u8() != 1
    {
        return Err("Bootstrap challenge verification failed: nonce mismatch".to_string());
    }

    if ready_msg.backend_nonce.len() < 32 {
        return Err("Backend nonce is insufficiently long".to_string());
    }

    // Step 3: Send BootstrapAuthorize
    let auth_token = generate_random_hex(32);
    let auth_msg = BootstrapAuthorize {
        auth_token: auth_token.clone(),
        backend_nonce_ack: ready_msg.backend_nonce,
    };
    let mut auth_json = serde_json::to_string(&auth_msg).map_err(|e| e.to_string())?;
    auth_json.push('\n');
    writer
        .write_all(auth_json.as_bytes())
        .await
        .map_err(|e| format!("Failed to send BootstrapAuthorize: {}", e))?;
    writer
        .flush()
        .await
        .map_err(|e| format!("Failed to flush BootstrapAuthorize: {}", e))?;

    // Step 4: Read BootstrapAck
    let ack_line = lines
        .next_line()
        .await
        .map_err(|e| format!("Failed to read BootstrapAck line: {}", e))?
        .ok_or_else(|| "Connection closed by backend before BootstrapAck".to_string())?;

    let ack_msg: BootstrapAck = serde_json::from_str(&ack_line)
        .map_err(|e| format!("Invalid BootstrapAck payload: {}: {}", e, ack_line))?;

    if ack_msg.status != "active" {
        return Err(format!(
            "Unexpected BootstrapAck status: {}",
            ack_msg.status
        ));
    }

    Ok((ready_msg.port, auth_token))
}

#[cfg(windows)]
pub fn create_windows_pipe_server(
    pipe_name: &str,
) -> Result<tokio::net::windows::named_pipe::NamedPipeServer, String> {
    use tokio::net::windows::named_pipe::ServerOptions;

    ServerOptions::new()
        .first_pipe_instance(true)
        .max_instances(1)
        .create(pipe_name)
        .map_err(|e| format!("Failed to create named pipe {}: {}", pipe_name, e))
}

#[cfg(windows)]
pub async fn complete_windows_pipe_handshake(
    server: tokio::net::windows::named_pipe::NamedPipeServer,
    expected_child_pid: u32,
) -> Result<(u16, String), String> {
    use std::os::windows::io::AsRawHandle;

    server
        .connect()
        .await
        .map_err(|e| format!("Failed waiting for named pipe client connection: {}", e))?;

    // Validate client PID
    let raw_handle = server.as_raw_handle();
    let mut client_pid: u32 = 0;
    let res = unsafe {
        windows_sys::Win32::System::Pipes::GetNamedPipeClientProcessId(
            raw_handle as _,
            &mut client_pid,
        )
    };
    if res == 0 {
        return Err("Failed to query GetNamedPipeClientProcessId".to_string());
    }

    if client_pid != expected_child_pid {
        return Err(format!(
            "Untrusted pipe client process PID: expected {}, got {}",
            expected_child_pid, client_pid
        ));
    }

    let (reader, writer) = tokio::io::split(server);
    perform_handshake_over_stream(reader, writer).await
}

#[cfg(windows)]
pub async fn run_windows_pipe_handshake(
    pipe_name: &str,
    expected_child_pid: u32,
) -> Result<(u16, String), String> {
    let server = create_windows_pipe_server(pipe_name)?;
    complete_windows_pipe_handshake(server, expected_child_pid).await
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_random_hex_generation() {
        let hex1 = generate_random_hex(32);
        let hex2 = generate_random_hex(32);
        assert_eq!(hex1.len(), 64);
        assert_eq!(hex2.len(), 64);
        assert_ne!(hex1, hex2);
    }

    #[test]
    fn test_pipe_name_format() {
        let name = generate_pipe_name();
        assert!(name.starts_with(r"\\.\pipe\postflow-bootstrap-"));
    }

    #[tokio::test]
    async fn test_handshake_protocol_success() {
        let (client_stream, server_stream) = tokio::io::duplex(4096);

        let server_task = tokio::spawn(async move {
            let (reader, writer) = tokio::io::split(server_stream);
            perform_handshake_over_stream(reader, writer).await
        });

        let client_task = tokio::spawn(async move {
            let (reader, mut writer) = tokio::io::split(client_stream);
            let mut lines = BufReader::new(reader).lines();

            // 1. Read BootstrapInit
            let init_line = lines.next_line().await.unwrap().unwrap();
            let init: BootstrapInit = serde_json::from_str(&init_line).unwrap();
            assert_eq!(init.protocol_version, 1);

            // 2. Send BootstrapReady
            let ready = BootstrapReady {
                echoed_challenge: init.challenge_nonce,
                port: 54321,
                backend_nonce: "aabbccddeeff00112233445566778899".to_string(),
            };
            let mut ready_str = serde_json::to_string(&ready).unwrap();
            ready_str.push('\n');
            writer.write_all(ready_str.as_bytes()).await.unwrap();
            writer.flush().await.unwrap();

            // 3. Read BootstrapAuthorize
            let auth_line = lines.next_line().await.unwrap().unwrap();
            let auth: BootstrapAuthorize = serde_json::from_str(&auth_line).unwrap();
            assert_eq!(auth.backend_nonce_ack, "aabbccddeeff00112233445566778899");
            assert_eq!(auth.auth_token.len(), 64);

            // 4. Send BootstrapAck
            let ack = BootstrapAck {
                status: "active".to_string(),
            };
            let mut ack_str = serde_json::to_string(&ack).unwrap();
            ack_str.push('\n');
            writer.write_all(ack_str.as_bytes()).await.unwrap();
            writer.flush().await.unwrap();

            auth.auth_token
        });

        let (server_res, client_res) = tokio::join!(server_task, client_task);
        let (port, server_token) = server_res.unwrap().expect("Server handshake failed");
        let client_token = client_res.unwrap();

        assert_eq!(port, 54321);
        assert_eq!(server_token, client_token);
    }

    #[tokio::test]
    async fn test_handshake_protocol_tampered_challenge() {
        let (client_stream, server_stream) = tokio::io::duplex(4096);

        let server_task = tokio::spawn(async move {
            let (reader, writer) = tokio::io::split(server_stream);
            perform_handshake_over_stream(reader, writer).await
        });

        let client_task = tokio::spawn(async move {
            let (reader, mut writer) = tokio::io::split(client_stream);
            let mut lines = BufReader::new(reader).lines();

            let _init_line = lines.next_line().await.unwrap().unwrap();
            let ready = BootstrapReady {
                echoed_challenge: "tampered_nonce_00000000000000000".to_string(),
                port: 54321,
                backend_nonce: "aabbccddeeff00112233445566778899".to_string(),
            };
            let mut ready_str = serde_json::to_string(&ready).unwrap();
            ready_str.push('\n');
            writer.write_all(ready_str.as_bytes()).await.unwrap();
            writer.flush().await.unwrap();
        });

        let (server_res, _) = tokio::join!(server_task, client_task);
        let err = server_res.unwrap().unwrap_err();
        assert!(err.contains("Bootstrap challenge verification failed"));
    }
}
