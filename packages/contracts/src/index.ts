/**
 * @postflow/contracts
 *
 * Authoritative shared types and IPC contracts between Tauri/Rust and React.
 * NOTE: Secrets and internal credentials must NEVER appear in these contracts.
 */

export interface BackendHealthResponse {
  status: 'ok' | 'degraded' | 'unavailable';
  version: string;
  environment: string;
  host: string;
}

export interface AppInfoResponse {
  name: string;
  version: string;
  tauriVersion: string;
  rustVersion?: string;
  platform: string;
  arch: string;
}

export interface ArchitectureLayerStatus {
  layer: 'desktop_shell' | 'frontend_ui' | 'backend_engine';
  name: string;
  tech: string;
  status: 'scaffolded' | 'ready' | 'pending';
  details: string;
}

export interface IpcResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
}
