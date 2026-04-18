@echo off
REM Mental Health Chatbot - Development Startup Script (Windows)
REM This script starts both the backend and frontend servers

echo ==========================================
echo Mental Health Chatbot - Development Mode
echo ==========================================
echo.

REM Check if backend directory exists
if not exist "mental_health_chatbot\backend" (
    echo Error: Backend directory not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Check if frontend directory exists
if not exist "react_web" (
    echo Error: Frontend directory not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Start Backend
echo [1/2] Starting Backend Server...
cd mental_health_chatbot\backend

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else if exist "..\venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call ..\venv\Scripts\activate.bat
)

REM Check if requirements are installed
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo Installing backend dependencies...
    pip install -r requirements.txt
)

REM Start backend server in new window
start "Mental Health Backend" cmd /k "python main.py"

echo Backend started
echo   URL: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.

REM Wait for backend to start
echo Waiting for backend to be ready...
timeout /t 3 /nobreak >nul

REM Start Frontend
cd ..\..\react_web
echo [2/2] Starting Frontend Server...

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)

REM Start frontend server in new window
start "Mental Health Frontend" cmd /k "npm run dev"

echo Frontend started
echo   URL: http://localhost:5173
echo.

echo ==========================================
echo All servers running!
echo ==========================================
echo.
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop the servers
echo.
pause
