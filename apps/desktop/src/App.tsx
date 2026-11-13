import React, { useEffect, useState } from 'react';
import { ArchitectureLayerStatus, BackendHealthResponse } from '@postflow/contracts';
import { Header } from './components/Header';
import { StatusCard } from './components/StatusCard';
import { getAppInfo, checkBackendHealth } from './services/tauri';
import { Shield, Lock, Radio, Activity, RefreshCw } from 'lucide-react';

const ARCHITECTURE_LAYERS: ArchitectureLayerStatus[] = [
  {
    layer: 'desktop_shell',
    name: 'Desktop Shell & Supervision',
    tech: 'Tauri 2 + Rust',
    status: 'scaffolded',
    details: 'Native window lifecycle, process supervisor, and secure OS credential storage boundary.',
  },
  {
    layer: 'frontend_ui',
    name: 'Presentation & UI Shell',
    tech: 'React 18 + TypeScript + Vite',
    status: 'scaffolded',
    details: 'Untrusted client shell strictly restricted to typed Tauri IPC commands without raw secrets.',
  },
  {
    layer: 'backend_engine',
    name: 'Backend Modular Monolith',
    tech: 'Python 3.11+ + FastAPI',
    status: 'scaffolded',
    details: 'Local engine bound strictly to 127.0.0.1 loopback with protected bootstrap protocol.',
  },
];

export const App: React.FC = () => {
  const [appInfo, setAppInfo] = useState<{ name: string; version: string; platform: string } | null>(null);
  const [health, setHealth] = useState<BackendHealthResponse | null>(null);
  const [isChecking, setIsChecking] = useState(false);

  useEffect(() => {
    getAppInfo().then((info) => setAppInfo(info));
  }, []);

  const handleCheckHealth = async () => {
    setIsChecking(true);
    try {
      const res = await checkBackendHealth();
      setHealth(res);
    } catch (err) {
      console.error('Health check failed:', err);
    } finally {
      setIsChecking(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      <Header />

      <main style={{ flex: 1, padding: '2rem', maxWidth: '1100px', margin: '0 auto', width: '100%' }}>
        {/* Intro */}
        <section style={{ marginBottom: '2rem' }}>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.5rem' }}>
            M1.1 Application Foundation Scaffold
          </h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9375rem', maxWidth: '750px' }}>
            PostFlow is established as a single-user, local-first desktop modular monolith.
            The foundation guarantees complete separation between frontend presentation,
            Rust lifecycle orchestration, and the local Python FastAPI backend engine.
          </p>
        </section>

        {/* Architecture Grid */}
        <section style={{ marginBottom: '2.5rem' }}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: 600, marginBottom: '1rem' }}>
            Modular Monolith Boundaries
          </h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
            {ARCHITECTURE_LAYERS.map((layer) => (
              <StatusCard key={layer.layer} status={layer} />
            ))}
          </div>
        </section>

        {/* Non-Negotiable Invariants */}
        <section style={{ marginBottom: '2.5rem' }}>
          <h3 style={{ fontSize: '1.125rem', fontWeight: 600, marginBottom: '1rem' }}>
            Architectural & Security Invariants
          </h3>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
              gap: '1rem',
              backgroundColor: 'var(--bg-secondary)',
              padding: '1.25rem',
              borderRadius: '0.75rem',
              border: '1px solid var(--border-color)',
            }}
          >
            <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
              <Radio size={20} color="var(--accent-color)" style={{ marginTop: '0.2rem', flexShrink: 0 }} />
              <div>
                <strong style={{ fontSize: '0.875rem' }}>Strict Loopback</strong>
                <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
                  Backend strictly binds to 127.0.0.1; non-loopback binds fail closed.
                </p>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
              <Lock size={20} color="var(--success-color)" style={{ marginTop: '0.2rem', flexShrink: 0 }} />
              <div>
                <strong style={{ fontSize: '0.875rem' }}>Zero Secret Exposure</strong>
                <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
                  Secrets stored in OS Credential Manager; React never receives raw tokens.
                </p>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
              <Shield size={20} color="var(--accent-color)" style={{ marginTop: '0.2rem', flexShrink: 0 }} />
              <div>
                <strong style={{ fontSize: '0.875rem' }}>Strict CSP & Typed IPC</strong>
                <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>
                  No remote scripts or arbitrary HTTP forwarding. Typed Tauri commands only.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Development Verification Panel */}
        <section
          style={{
            backgroundColor: 'var(--bg-card)',
            border: '1px solid var(--border-color)',
            borderRadius: '0.75rem',
            padding: '1.5rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Activity size={18} color="var(--accent-color)" />
              <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>Development Verification</h3>
            </div>
            <button
              onClick={handleCheckHealth}
              disabled={isChecking}
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.4rem',
                backgroundColor: 'var(--accent-color)',
                color: '#0f172a',
                padding: '0.4rem 0.85rem',
                borderRadius: '0.375rem',
                fontWeight: 600,
                fontSize: '0.8125rem',
              }}
            >
              <RefreshCw size={14} className={isChecking ? 'spin' : ''} />
              {isChecking ? 'Checking...' : 'Check Health'}
            </button>
          </div>

          <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)', display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.75rem' }}>
            <div>
              <strong>App Runtime:</strong> {appInfo ? `${appInfo.name} v${appInfo.version} (${appInfo.platform})` : 'Loading...'}
            </div>
            <div>
              <strong>Backend Status:</strong>{' '}
              {health ? `${health.status} (${health.host}) — M1.1 Dev Scaffold` : 'Unchecked (click Check Health)'}
            </div>
          </div>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.75rem', marginBottom: 0 }}>
            * Development scaffold: Supervised child process lifecycle and protected bootstrap handshake arrive in M1.2.
          </p>
        </section>
      </main>

      <footer
        style={{
          padding: '1rem 2rem',
          textAlign: 'center',
          fontSize: '0.75rem',
          color: 'var(--text-muted)',
          borderTop: '1px solid var(--border-color)',
        }}
      >
        PostFlow Desktop Shell — M1.1 Application Foundation | Local-First Architecture
      </footer>
    </div>
  );
};
