@echo off
REM MedCare - Complete Setup & Start Guide

:INIT
cls
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║         MedCare Healthcare Application Setup               ║
echo ║                  Version 1.0                               ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python is NOT installed or not in PATH
    echo.
    echo ACTION REQUIRED:
    echo 1. Download Python from https://www.python.org/
    echo 2. Install Python 3.8 or higher
    echo 3. IMPORTANT: Check "Add Python to PATH" during installation
    echo 4. Restart your computer
    echo 5. Run this script again
    echo.
    pause
    exit /b 1
)

echo ✓ Python is installed
python --version
echo.

REM Create venv if needed
if not exist "myenv" (
    echo Creating virtual environment...
    python -m venv myenv
    if errorlevel 1 (
        echo ✗ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
    echo.
)

REM Activate venv
call myenv\Scripts\activate.bat

REM Install packages
echo Installing required packages...
pip install -q flask pandas joblib scikit-learn

echo ✓ All packages installed
echo.

REM Try simple app first
echo.
echo ════════════════════════════════════════════════════════════
echo Attempting to start simplified application...
echo ════════════════════════════════════════════════════════════
echo.

python app_simple.py

REM If that failed
if errorlevel 1 (
    echo.
    echo ✗ Application failed to start!
    echo.
    echo TROUBLESHOOTING:
    echo 1. Run: python test_startup.py
    echo 2. Check if port 5000 is in use
    echo 3. Try different port: edit config.py and change PORT
    echo.
    pause
    exit /b 1
)
