@echo off
echo.
echo ========================================
echo   MedCare Healthcare Application
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "myenv" (
    echo Creating virtual environment...
    python -m venv myenv
    echo ✓ Virtual environment created
    echo.
)

REM Activate virtual environment
call myenv\Scripts\activate.bat

REM Check if dependencies are installed
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo ✓ Dependencies installed
    echo.
)

echo Starting application...
echo.
echo 🚀 Application running at: http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the application
echo.

python main.py
