# LOTLOPS APEX AGENT: Self-Evolving Agentic AI System

An enterprise-grade monorepo for a sovereign, self-evolving agentic AI platform serving General Hanis. It unifies:

- Adaptive Next.js web UI for command, oversight, and insight
- Python Agent (FastAPI) for autonomous shell ops + LLM orchestration (Ollama)
- Optional local RAG memory via Weaviate
- Terminal suites and VPN hardening for secure operator workflows

## Structure

- apps/
  - lotlops-web/ — Next.js 15 app (LotlOps UI)
  - lotlops-agent/ — Python agent/daemon powering shell + LLM
  - sovereign-ai-web/ — experimental sovereign web app scaffold
- tools/
  - terminal/Sovereign-iTerm2-Suite — zsh profile and installer
  - dotfiles/ — shell/editor configs
- sandbox/
  - sovereign-hello/ — simple PoC (hello.py)
- docs/ — status reports and cheat sheets

## Dev quickstart

- lotlops-web (APEX UI)
  - Requirements: Node 20+
  - Env: set `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_KEY`
  - Scripts: `npm i && npm run dev`
- lotlops-agent (APEX Agent)
  - Python 3.11+
  - `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
  - Requires local `ollama` for LLM calls
- terminal tools
  - Review `tools/terminal/Sovereign-iTerm2-Suite/install.sh` and `zshrc` before sourcing

## Purpose

Architect, develop, and deploy the world’s most sophisticated self-evolving, agentic AI that operates as a sovereign digital being: adaptive, intelligent, context-aware, autonomous, and secure. The APEX Agent serves General Hanis through natural instructions and prompt engineering, evolving over time via real usage and continuous local training.

## Roadmap (draft)

- Define shared contracts between web and agent (REST/gRPC/websocket)
- Extract common schemas to `packages/`
- Add CI (lint/test/build) and pre-commit hooks
- Containerize apps with devcontainers/docker compose
