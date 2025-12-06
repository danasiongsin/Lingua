#!/bin/bash

# Lingua Development Startup Script
# This script starts both the backend and frontend servers

echo "🌍 Starting Lingua Development Environment..."
echo ""

# Check if we're in the right directory
if [ ! -d "client-safe" ] || [ ! -d "server" ]; then
    echo "❌ Error: Please run this script from the Lingua project root directory"
    exit 1
fi

# Check for sample videos
if [ ! -f "client-safe/public/videos/english-sample.mp4" ] || \
   [ ! -f "client-safe/public/videos/spanish-sample.mp4" ] || \
   [ ! -f "client-safe/public/videos/french-sample.mp4" ]; then
    echo "⚠️  Warning: Sample videos not found in client-safe/public/videos/"
    echo "   Please add the following files:"
    echo "   - english-sample.mp4"
    echo "   - spanish-sample.mp4"
    echo "   - french-sample.mp4"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for LLM_API_KEY
if [ -z "$LLM_API_KEY" ]; then
    echo "⚠️  Warning: LLM_API_KEY environment variable is not set"
    echo "   The backend may not work properly without it"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "Starting backend server..."
cd server
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

echo "Backend started with PID: $BACKEND_PID"
echo ""

# Wait a bit for backend to start
sleep 3

echo "Starting frontend server..."
cd client-safe
npm run dev &
FRONTEND_PID=$!
cd ..

echo "Frontend started with PID: $FRONTEND_PID"
echo ""
echo "✅ Development servers are running!"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup INT TERM

# Wait for both processes
wait
