#!/bin/bash

pkill -f "python app.py" 2>/dev/null
pkill -f "http.server" 2>/dev/null

echo "Starting Nexvora NexGen AI..."

# Backend
(cd backend && BACKEND_PORT=5050 python app.py &)
sleep 2

# Frontend
(cd frontend && python -m http.server 8000 &)
sleep 2

echo "Backend: http://127.0.0.1:5050"
echo "Frontend: http://127.0.0.1:8000"
echo "Press CTRL+C to stop everything."

wait
