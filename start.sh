#!/bin/bash

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example"
    cp .env.example .env
fi

# Create database directory if it doesn't exist
mkdir -p src/models

echo "Starting FastAPI server..."
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
