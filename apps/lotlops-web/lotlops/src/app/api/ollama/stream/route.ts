import crypto from 'crypto';
import { NextRequest } from 'next/server';

export const runtime = 'edge';

export async function GET(req: NextRequest) {
  const prompt = req.nextUrl.searchParams.get('prompt') || '';
  const agentBase = (process.env.AGENT_URL || 'http://localhost:8000').replace(/\/$/, '');
  const agentSecret = process.env.AGENT_SHARED_SECRET || 'change-me';

  const body = JSON.stringify({ prompt });
  const ts = Math.floor(Date.now() / 1000).toString();
  const sig = crypto.createHmac('sha256', agentSecret).update(ts + '.' + body).digest('hex');

  const res = await fetch(agentBase + '/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-timestamp': ts,
      'x-signature': sig,
    },
    body,
  });
  return new Response(res.body, { headers: { 'Content-Type': 'text/event-stream' } });
}
