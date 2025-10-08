#!/bin/bash
# LOTL-APEX Terminal Interface Runner

cd "$(dirname "$0")/.."

echo "🎯 Starting LOTL-APEX Terminal Interface..."

# Start the Python terminal app
python3 scripts/terminal_app.py
