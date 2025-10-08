export default function Home() {
  return (
    <main className="min-h-screen bg-gray-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-6">LOTL Apex</h1>
        <p className="text-xl text-gray-300 mb-8">
          Sovereign AI System with Multi-Agent Architecture
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-gray-800 p-6 rounded-lg">
            <h2 className="text-xl font-semibold mb-3">🤖 Agent Swarm</h2>
            <p className="text-gray-400">
              6 specialized AI agents working in coordination
            </p>
          </div>
          
          <div className="bg-gray-800 p-6 rounded-lg">
            <h2 className="text-xl font-semibold mb-3">🧠 Identity Engine</h2>
            <p className="text-gray-400">
              AI that learns and adapts to your patterns
            </p>
          </div>
          
          <div className="bg-gray-800 p-6 rounded-lg">
            <h2 className="text-xl font-semibold mb-3">🔍 OSINT Suite</h2>
            <p className="text-gray-400">
              Advanced reconnaissance and investigation tools
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
