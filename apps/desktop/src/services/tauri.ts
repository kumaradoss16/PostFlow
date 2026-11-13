/**
 * Tauri IPC service wrapper.
 *
 * All desktop-to-backend communication strictly travels through typed Tauri IPC.
 * React NEVER makes direct HTTP requests or manages secrets.
 */

import {
  AppInfoResponse,
  BackendHealthResponse,
  BackendProxyRequest,
  BackendProxyResponse,
  SupervisorStatus,
} from '@postflow/contracts';

// Safe check if running inside Tauri window
export function isTauriEnvironment(): boolean {
  return typeof window !== 'undefined' && '__TAURI_INTERNALS__' in window;
}

export async function getAppInfo(): Promise<AppInfoResponse> {
  if (isTauriEnvironment()) {
    try {
      const { invoke } = await import('@tauri-apps/api/core');
      return await invoke<AppInfoResponse>('get_app_info');
    } catch (err) {
      console.warn('Failed to invoke get_app_info from Tauri, falling back to mock:', err);
    }
  }

  // Development fallback for standalone Vite browser inspection
  return {
    name: 'PostFlow',
    version: '0.1.0',
    tauriVersion: '2.x (development)',
    platform: 'windows',
    arch: 'x86_64',
  };
}

export async function getBackendStatus(): Promise<SupervisorStatus> {
  if (isTauriEnvironment()) {
    try {
      const { invoke } = await import('@tauri-apps/api/core');
      return await invoke<SupervisorStatus>('backend_get_status');
    } catch (err) {
      console.warn('Failed to invoke backend_get_status from Tauri:', err);
    }
  }

  return {
    state: 'ready',
    port: 8000,
    pid: 12345,
    uptimeSeconds: 42,
  };
}

export async function startBackend(): Promise<SupervisorStatus> {
  if (isTauriEnvironment()) {
    const { invoke } = await import('@tauri-apps/api/core');
    return await invoke<SupervisorStatus>('backend_start');
  }

  return {
    state: 'ready',
    port: 8000,
    pid: 12345,
    uptimeSeconds: 1,
  };
}

export async function stopBackend(): Promise<SupervisorStatus> {
  if (isTauriEnvironment()) {
    const { invoke } = await import('@tauri-apps/api/core');
    return await invoke<SupervisorStatus>('backend_stop');
  }

  return {
    state: 'stopped',
  };
}

export async function proxyBackendRequest<T = unknown>(
  request: BackendProxyRequest
): Promise<BackendProxyResponse<T>> {
  if (isTauriEnvironment()) {
    const { invoke } = await import('@tauri-apps/api/core');
    return await invoke<BackendProxyResponse<T>>('backend_proxy_request', { request });
  }

  // Browser development fallback
  if (request.path === '/api/v1/health') {
    return {
      statusCode: 200,
      data: {
        status: 'ok',
        version: '0.1.0',
        environment: 'development',
        host: '127.0.0.1',
      } as T,
    };
  }

  return {
    statusCode: 200,
    data: {} as T,
  };
}

export async function checkBackendHealth(): Promise<BackendHealthResponse> {
  if (isTauriEnvironment()) {
    try {
      const { invoke } = await import('@tauri-apps/api/core');
      return await invoke<BackendHealthResponse>('check_backend_health');
    } catch (err) {
      console.warn('Failed to invoke check_backend_health, fallback to proxy:', err);
      const res = await proxyBackendRequest<BackendHealthResponse>({
        method: 'GET',
        path: '/api/v1/health',
      });
      if (res.data) {
        return res.data;
      }
      throw new Error(res.error || 'Health check failed');
    }
  }

  // Development simulation for browser mode
  return {
    status: 'ok',
    version: '0.1.0',
    environment: 'development',
    host: '127.0.0.1',
  };
}
