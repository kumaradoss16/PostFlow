import React from 'react';
import { ArchitectureLayerStatus } from '@postflow/contracts';
import { CheckCircle2, Clock } from 'lucide-react';

interface StatusCardProps {
  status: ArchitectureLayerStatus;
}

export const StatusCard: React.FC<StatusCardProps> = ({ status }) => {
  const isReady = status.status === 'ready' || status.status === 'scaffolded';

  return (
    <div
      style={{
        backgroundColor: 'var(--bg-card)',
        border: '1px solid var(--border-color)',
        borderRadius: '0.75rem',
        padding: '1.25rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '0.75rem',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>{status.name}</h3>
        <span
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.25rem',
            fontSize: '0.75rem',
            padding: '0.2rem 0.5rem',
            borderRadius: '0.375rem',
            backgroundColor: isReady ? 'var(--success-subtle)' : 'var(--warning-subtle)',
            color: isReady ? 'var(--success-color)' : 'var(--warning-color)',
            fontWeight: 500,
          }}
        >
          {isReady ? <CheckCircle2 size={13} /> : <Clock size={13} />}
          {status.status.toUpperCase()}
        </span>
      </div>

      <div style={{ fontSize: '0.8125rem', color: 'var(--text-secondary)' }}>
        <strong>Technology:</strong> {status.tech}
      </div>

      <p style={{ fontSize: '0.8125rem', color: 'var(--text-muted)' }}>{status.details}</p>
    </div>
  );
};
