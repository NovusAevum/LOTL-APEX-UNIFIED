'use client'
import { useState } from 'react'

export default function MemoryPage() {
  const [q, setQ] = useState('')
  const [results, setResults] = useState<any[]>([])

  async function run() {
    const res = await fetch('/api/memory/search', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ q }) })
    const data = await res.json()
    setResults(data.results || [])
  }

  return (
    <main className="p-6 text-sm">
      <h1 className="text-xl font-semibold mb-4">Memory</h1>
      <div className="flex gap-2 mb-3">
        <input className="bg-zinc-900 border border-zinc-700 rounded px-2 py-1 w-full" value={q} onChange={e => setQ(e.target.value)} placeholder="search memory..." />
        <button onClick={run} className="border border-zinc-700 rounded px-3">Search</button>
      </div>
      <ul className="space-y-2">
        {results.map((r: any, i: number) => (
          <li key={i} className="border border-zinc-700 rounded p-3">
            <div className="opacity-80 whitespace-pre-wrap">{r.content}</div>
            <div className="text-xs opacity-60 mt-1">{r.created_at}</div>
          </li>
        ))}
      </ul>
    </main>
  )
}
