import type { ReactNode } from 'react';

export const metadata = {
  title: 'AgentForge',
  description: 'Multi-agent orchestration dashboard',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: 'Inter, system-ui, sans-serif', margin: 0 }}>
        <header style={{ padding: '12px 16px', borderBottom: '1px solid #e5e7eb' }}>
          <strong>AgentForge</strong>
        </header>
        <div style={{ padding: '16px' }}>{children}</div>
      </body>
    </html>
  );
}
