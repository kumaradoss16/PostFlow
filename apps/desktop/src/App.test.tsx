import { describe, it, expect } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { App } from './App';

describe('PostFlow Application Shell', () => {
  it('renders PostFlow branding and header', async () => {
    await act(async () => {
      render(<App />);
    });
    expect(screen.getByText('PostFlow')).toBeInTheDocument();
    expect(screen.getByText('M1.1 Application Foundation')).toBeInTheDocument();
  });

  it('renders the modular monolith architecture status cards', async () => {
    await act(async () => {
      render(<App />);
    });
    expect(screen.getByText('Desktop Shell & Supervision')).toBeInTheDocument();
    expect(screen.getByText('Presentation & UI Shell')).toBeInTheDocument();
    expect(screen.getByText('Backend Modular Monolith')).toBeInTheDocument();
  });

  it('renders non-negotiable architectural invariant indicators', async () => {
    await act(async () => {
      render(<App />);
    });
    expect(screen.getByText('Strict Loopback')).toBeInTheDocument();
    expect(screen.getByText('Zero Secret Exposure')).toBeInTheDocument();
    expect(screen.getByText('Strict CSP & Typed IPC')).toBeInTheDocument();
  });

  it('renders development verification panel with M1.2 boundary disclaimer', async () => {
    await act(async () => {
      render(<App />);
    });
    expect(screen.getByText('Development Verification')).toBeInTheDocument();
    expect(
      screen.getByText(/Development scaffold: Supervised child process lifecycle/i)
    ).toBeInTheDocument();
  });
});
