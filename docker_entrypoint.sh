#!/bin/sh
echo "Starting pre-commit install..."
pre-commit install &
echo "Starting admin module..."
fastapi run app/main.py --host 0.0.0.0 --port 8000