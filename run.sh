#!/bin/bash

echo "🚀 Starting Nexvora AI..."

cd backend
python app.py &

cd ../frontend
python -m http.server 8000
