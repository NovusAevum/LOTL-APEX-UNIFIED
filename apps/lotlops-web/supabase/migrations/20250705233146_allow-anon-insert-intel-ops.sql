-- Enable Row Level Security
alter table public.intel_ops enable row level security;

-- Create a policy to allow anon insert
create policy "Allow anon insert" on public.intel_ops
for insert
to anon
with check (true);

-- supabase/migrations/XXXX_create-intel-ops-table.sql

create extension if not exists "uuid-ossp";

create table if not exists public.intel_ops (
  id uuid primary key default uuid_generate_v4(),
  title text not null,
  description text,
  created_at timestamptz default now()
);
