#!/bin/bash

# Optimized startup script for 500MB deployment

echo "🚀 Starting QWalT Backend (Optimized for 500MB RAM)"

# Set memory-optimized Python flags
export PYTHONOPTIMIZE=2
export PYTHONDONTWRITEBYTECODE=1
export PYTHONUNBUFFERED=1

# Limit Python memory usage
export MALLOC_TRIM_THRESHOLD_=100000

# Start with optimized settings
exec uvicorn app:app \
    --host 0.0.0.0 \
    --port ${PORT:-8000} \
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload \
    --access-log \
    --log-level info
