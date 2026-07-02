@echo off
REM MedCare - Quick Debug Start
echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║           MedCare - Quick Debug Startup                    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check if venv exists
if not exist "myenv" (
    echo Creating virtual environment...
    python -m venv myenv
    echo.
)

REM Activate venv
call myenv\Scripts\activate.bat

REM Install requirements silently
echo Installing dependencies...
pip install -q flask pandas joblib scikit-learn 2>nul

echo.
echo Starting simplified app (shows all errors)...
echo.

REM Run the simple app
python app_simple.py

REM If that fails, show error
if errorlevel 1 (
    echo.
    echo ✗ Failed to start!
    echo.
    echo Run diagnostics:
    echo   python test_startup.py
    echo.
    pause
)
