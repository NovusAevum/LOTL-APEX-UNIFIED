export default async function TasksPage() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL || ''}/api/tasks`, { cache: 'no-store' });
  const data = await res.json();
  const tasks = data.tasks || [];
  return (
    <main className="p-6 text-sm">
      <h1 className="text-xl font-semibold mb-4">Tasks</h1>
      <ul className="space-y-2">
        {tasks.map((t: any) => (
          <li key={t.id} className="border border-zinc-700 rounded p-3">
            <div className="font-medium">{t.title}</div>
            <div className="opacity-80">{t.description}</div>
            <div className="mt-1 text-xs opacity-70">status: {t.status} · priority: {t.priority}</div>
          </li>
        ))}
      </ul>
    </main>
  );
}
