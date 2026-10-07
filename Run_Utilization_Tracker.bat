@echo off
setlocal enabledelayedexpansion
title Finance Team Utilization Tracker

echo ==========================================================
echo       Finance Team Utilization Tracker Launcher
echo ==========================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python was not found in your system PATH.
    echo Please install Python 3.11+ from https://www.python.org/
    echo and check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking and creating required directories...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "exports" mkdir exports

echo [2/3] Checking dependencies from requirements.txt...
python -m pip install -r requirements.txt --quiet --no-warn-script-location
if %errorlevel% neq 0 (
    echo [WARNING] Encountered an issue while installing packages. Retrying in verbose mode...
    python -m pip install -r requirements.txt
)

echo [3/3] Launching Utilization Tracker Streamlit Application...
echo.
echo Application will open in your default browser at http://localhost:8501
echo Press Ctrl+C in this terminal window to stop the server.
echo ==========================================================
echo.

python -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false

pause
