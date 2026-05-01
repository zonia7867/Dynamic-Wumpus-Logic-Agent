@echo off
REM Setup and run script for Wumpus World Agent
REM This script installs dependencies and starts both backend and frontend

echo ===============================================
echo Wumpus World - Dynamic Logic Agent
echo ===============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Python found. Continuing...
echo.

REM Navigate to backend and install requirements
echo [1] Installing Python dependencies...
cd backend
pip install -r requirements.txt

if errorlevel 1 (
    echo Error installing dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully!
echo.

REM Start backend
echo [2] Starting Flask backend server...
start cmd /k python app.py

REM Wait a moment for backend to start
timeout /t 2 /nobreak

REM Navigate to frontend
cd ..\frontend

echo [3] Starting frontend server...
echo.
echo Opening browser...
start cmd /k python -m http.server 8000
timeout /t 2 /nobreak

echo.
echo ===============================================
echo Setup Complete!
echo ===============================================
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8000
echo.
echo Your browser should open automatically.
echo If not, visit: http://localhost:8000
echo.
pause
