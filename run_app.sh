#!/bin/bash

# Setup and run script for Wumpus World Agent (Linux/Mac)

echo "==============================================="
echo "Wumpus World - Dynamic Logic Agent"
echo "==============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "Python found. Continuing..."
echo ""

# Navigate to backend and install requirements
echo "[1] Installing Python dependencies..."
cd backend
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error installing dependencies"
    exit 1
fi

echo "Dependencies installed successfully!"
echo ""

# Start backend in background
echo "[2] Starting Flask backend server..."
python3 app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Navigate to frontend
cd ../frontend

echo "[3] Starting frontend server..."
echo ""
echo "Opening browser..."
python3 -m http.server 8000 &
FRONTEND_PID=$!

# Wait a moment then open browser
sleep 2

# Try to open browser (works on Mac and Linux)
if command -v open &> /dev/null; then
    open http://localhost:8000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8000
fi

echo ""
echo "==============================================="
echo "Setup Complete!"
echo "==============================================="
echo ""
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:8000"
echo ""
echo "If browser didn't open, visit: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for user to terminate
wait $BACKEND_PID $FRONTEND_PID
