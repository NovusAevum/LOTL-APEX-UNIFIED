import crypto from 'crypto';
import { NextRequest } from 'next/server';

export const runtime = 'edge';

export async function POST(req: NextRequest) {
  try {
    const { instruction } = await req.json();
    if (!instruction) {
      return new Response(JSON.stringify({ error: 'instruction is required' }), { status: 400 });
    }

    const agentUrl = (process.env.AGENT_URL || 'http://localhost:8000/invoke').replace('/invoke', '/partner');
    const agentSecret = process.env.AGENT_SHARED_SECRET || 'change-me';

    const body = JSON.stringify({ instruction });
    const ts = Math.floor(Date.now() / 1000).toString();
    const sig = crypto.createHmac('sha256', agentSecret).update(ts + '.' + body).digest('hex');

    const res = await fetch(agentUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-timestamp': ts,
        'x-signature': sig,
      },
      body,
    });

    if (!res.ok) {
      const text = await res.text();
      return new Response(JSON.stringify({ error: `partner error: ${text}` }), { status: 502 });
    }

    const data = await res.json();
    return new Response(JSON.stringify(data), { headers: { 'Content-Type': 'application/json' } });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err?.message || 'unknown error' }), { status: 500 });
  }
}
