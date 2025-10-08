import crypto from 'crypto';
import { NextRequest } from 'next/server';

export const runtime = 'edge';

export async function GET() {
  const agentUrl = (process.env.AGENT_URL || 'http://localhost:8000').replace(/\/$/, '') + '/tasks';
  const agentSecret = process.env.AGENT_SHARED_SECRET || 'change-me';
  const ts = Math.floor(Date.now() / 1000).toString();
  const sig = crypto.createHmac('sha256', agentSecret).update(ts + '.').digest('hex');
  const res = await fetch(agentUrl, { headers: { 'x-timestamp': ts, 'x-signature': sig } });
  const data = await res.json();
  return new Response(JSON.stringify(data), { headers: { 'Content-Type': 'application/json' } });
}
