#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export PYTHONPATH=.
exec uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
