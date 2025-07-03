@echo off
REM SignalTap FastAPI Backend Runner Script for Windows
REM This script activates the virtual environment and runs the FastAPI application

echo 🚀 Starting SignalTap FastAPI Backend...

REM Check if virtual environment exists
if not exist ".venv" (
    echo 📦 Virtual environment not found. Creating one...
    python -m venv .venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
)

REM Run the FastAPI application
echo 🌐 Starting FastAPI server...
echo 📖 API Documentation will be available at: http://localhost:8000/docs
echo 🔍 Interactive API docs at: http://localhost:8000/redoc
echo 🏥 Health check at: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 