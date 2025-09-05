export const dynamic = 'force-dynamic';

export async function GET() {
  const base = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
  try {
    const res = await fetch(`${base}/health`, { cache: 'no-store' });
    const data = await res.json().catch(() => ({ status: 'error' }));
    return new Response(JSON.stringify(data), {
      status: res.ok ? 200 : res.status,
      headers: { 'content-type': 'application/json' },
    });
  } catch {
    return new Response(JSON.stringify({ status: 'offline' }), {
      status: 503,
      headers: { 'content-type': 'application/json' },
    });
  }
}

