#!/bin/bash
export PYTHONPATH=.
echo "Starting Backend on http://localhost:8000"
uvicorn backend.main:app --host 0.0.0.0 --port 8000
