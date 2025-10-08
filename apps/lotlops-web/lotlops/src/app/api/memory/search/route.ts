import crypto from 'crypto';
import { NextRequest } from 'next/server';

export const runtime = 'edge';

export async function POST(req: NextRequest) {
  const { q, limit } = await req.json();
  const agentUrl = (process.env.AGENT_URL || 'http://localhost:8000').replace(/\/$/, '') + '/memory/search';
  const agentSecret = process.env.AGENT_SHARED_SECRET || 'change-me';
  const body = JSON.stringify({ q, limit });
  const ts = Math.floor(Date.now() / 1000).toString();
  const sig = crypto.createHmac('sha256', agentSecret).update(ts + '.' + body).digest('hex');
  const res = await fetch(agentUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-timestamp': ts, 'x-signature': sig },
    body,
  });
  const data = await res.json();
  return new Response(JSON.stringify(data), { headers: { 'Content-Type': 'application/json' } });
}
