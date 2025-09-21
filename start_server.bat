@echo off
echo 🚀 CodeMate Terminal Web Edition - Local Server
echo ================================================
echo Starting local server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.6+ and try again
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "api\terminal.py" (
    echo ❌ Error: api\terminal.py not found
    echo Make sure you're running this from the maccodemate directory
    pause
    exit /b 1
)

if not exist "public\index.html" (
    echo ❌ Error: public\index.html not found
    echo Make sure you're running this from the maccodemate directory
    pause
    exit /b 1
)

REM Start the server
echo ✅ Starting CodeMate Terminal Web Server...
echo 🌐 The terminal will open in your browser automatically
echo 🛑 Press Ctrl+C to stop the server
echo.

python run_local_server.py

pause
