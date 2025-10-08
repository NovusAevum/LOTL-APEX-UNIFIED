-- Enable uuid extension (if not exists)
create extension if not exists "uuid-ossp";

-- Create intel_ops table
create table public.intel_ops (
  id uuid primary key default uuid_generate_v4(),
  title text not null,
  description text,
  created_at timestamptz default now()
);

-- Enable Row Level Security
alter table public.intel_ops enable row level security;
