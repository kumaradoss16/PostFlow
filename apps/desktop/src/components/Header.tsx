import React from 'react';
import { Layers, ShieldCheck } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '1.25rem 2rem',
        borderBottom: '1px solid var(--border-color)',
        backgroundColor: 'var(--bg-secondary)',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            width: '2.5rem',
            height: '2.5rem',
            borderRadius: '0.5rem',
            backgroundColor: 'var(--accent-subtle)',
            color: 'var(--accent-color)',
          }}
        >
          <Layers size={22} />
        </div>
        <div>
          <h1 style={{ fontSize: '1.25rem', fontWeight: 700, letterSpacing: '-0.02em' }}>
            PostFlow
          </h1>
          <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            Single-User Local-First Desktop Engine
          </p>
        </div>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
        <span
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.35rem',
            padding: '0.3rem 0.75rem',
            borderRadius: '9999px',
            fontSize: '0.75rem',
            fontWeight: 600,
            backgroundColor: 'var(--success-subtle)',
            color: 'var(--success-color)',
            border: '1px solid rgba(34, 197, 94, 0.3)',
          }}
        >
          <ShieldCheck size={14} />
          M1.1 Application Foundation
        </span>
      </div>
    </header>
  );
};
