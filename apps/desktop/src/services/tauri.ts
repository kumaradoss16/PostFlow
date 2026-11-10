/**
 * Tauri IPC service wrapper.
 *
 * All desktop-to-backend communication strictly travels through typed Tauri IPC.
 * React NEVER makes direct HTTP requests or manages secrets.
 */

import { AppInfoResponse, BackendHealthResponse } from '@postflow/contracts';

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

export async function checkBackendHealth(): Promise<BackendHealthResponse> {
  if (isTauriEnvironment()) {
    try {
      const { invoke } = await import('@tauri-apps/api/core');
      return await invoke<BackendHealthResponse>('check_backend_health');
    } catch (err) {
      console.warn('Failed to invoke check_backend_health, fallback:', err);
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
