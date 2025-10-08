-- Create agents table
create table if not exists agents (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  avatar text,
  created_at timestamptz default now()
);

-- Create messages table
create table if not exists messages (
  id uuid primary key default gen_random_uuid(),
  agent_id uuid references agents(id) on delete cascade,
  content text not null,
  created_at timestamptz default now()
);

-- Enable RLS
alter table agents enable row level security;
alter table messages enable row level security;

-- Policies for agents
create policy "Allow anon insert" on agents for insert to anon with check (true);
create policy "Allow anon select" on agents for select to anon using (true);

-- Policies for messages
create policy "Allow anon insert" on messages for insert to anon with check (true);
create policy "Allow anon select" on messages for select to anon using (true);
