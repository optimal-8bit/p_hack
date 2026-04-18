@echo off
echo 🔄 Restarting Backend with Cache Clear
echo ========================================

REM Kill any existing Python processes running main.py
echo 1. Stopping existing backend...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq main.py*" 2>nul
if errorlevel 1 echo    No existing backend found

REM Clear Python cache
echo 2. Clearing Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
echo    ✅ Cache cleared

REM Wait a moment
timeout /t 2 /nobreak >nul

REM Start backend
echo 3. Starting backend...
python main.py
