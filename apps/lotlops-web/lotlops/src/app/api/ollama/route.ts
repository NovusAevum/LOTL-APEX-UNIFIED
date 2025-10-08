import { NextRequest } from 'next/server';
import crypto from 'crypto';

export const runtime = 'edge';

export async function POST(req: NextRequest) {
  try {
    const { prompt, model } = await req.json();
    if (!prompt) {
      return new Response(JSON.stringify({ error: 'prompt is required' }), { status: 400 });
    }

    const ollamaUrl = process.env.OLLAMA_URL || 'http://localhost:11434/api/generate';
    const ollamaModel = model || process.env.OLLAMA_MODEL || 'llama3';
    const agentUrl = process.env.AGENT_URL || 'http://localhost:8000/invoke';
    const agentSecret = process.env.AGENT_SHARED_SECRET || 'change-me';

    // Prefer agent proxy with HMAC auth to keep policies centralized
    const body = JSON.stringify({ prompt, model: ollamaModel });
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
      return new Response(JSON.stringify({ error: `ollama error: ${text}` }), { status: 502 });
    }

    const data = await res.json();
    return new Response(JSON.stringify({ output: data.output ?? data }), {
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err: any) {
    return new Response(JSON.stringify({ error: err?.message || 'unknown error' }), { status: 500 });
  }
}
