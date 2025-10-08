"use client";
import { useEffect, useRef, useState } from "react";

export default function StreamPage() {
  const [prompt, setPrompt] = useState("");
  const [output, setOutput] = useState("");
  const evtRef = useRef<EventSource | null>(null);

  function start() {
    if (evtRef.current) evtRef.current.close();
    setOutput("");
    // server proxy: /api/ollama/stream
    const url = `/api/ollama/stream?prompt=${encodeURIComponent(prompt)}`;
    const es = new EventSource(url);
    evtRef.current = es;
    es.onmessage = (e) => {
      setOutput((p) => p + e.data + "\n");
    };
    es.onerror = () => {
      es.close();
      evtRef.current = null;
    };
  }

  useEffect(() => () => evtRef.current?.close(), []);

  return (
    <main className="p-6 text-sm">
      <h1 className="text-xl font-semibold mb-4">Streaming</h1>
      <div className="flex gap-2 mb-3">
        <input className="bg-zinc-900 border border-zinc-700 rounded px-2 py-1 w-full" value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Enter prompt..." />
        <button onClick={start} className="border border-zinc-700 rounded px-3">Start</button>
      </div>
      <pre className="border border-zinc-700 rounded p-3 whitespace-pre-wrap">{output}</pre>
    </main>
  );
}
