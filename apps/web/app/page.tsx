'use client';

import { useEffect, useState } from 'react';

export default function Page() {
  const [status, setStatus] = useState<'unknown' | 'online' | 'offline'>('unknown');

  useEffect(() => {
    fetch(`/api/health`)
      .then((r) => (r.ok ? setStatus('online') : setStatus('offline')))
      .catch(() => setStatus('offline'));
  }, []);

  return (
    <main>
      <h1 style={{ marginBottom: 8 }}>Welcome to AgentForge</h1>
      <p>Multi-agent orchestration dashboard (MVP)</p>
      <div
        style={{
          marginTop: 16,
          padding: 12,
          border: '1px solid #e5e7eb',
          borderRadius: 12,
          display: 'inline-block',
        }}
      >
        <strong>Backend status:</strong>{' '}
        <span
          aria-live="polite"
          style={{
            padding: '2px 8px',
            borderRadius: 8,
            marginLeft: 8,
            border: '1px solid #e5e7eb',
          }}
        >
          {status}
        </span>
      </div>
    </main>
  );
}
