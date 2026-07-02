@echo off
REM MedCare Application - Setup and Startup

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║           MedCare Healthcare Application                   ║
echo ║         Automated Setup and Startup Script                 ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ✗ Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✓ Python is installed
echo.

REM Create virtual environment if it doesn't exist
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

REM Activate virtual environment
echo Activating virtual environment...
call myenv\Scripts\activate.bat
if errorlevel 1 (
    echo ✗ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

REM Install dependencies
echo Checking and installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo ✗ Failed to install dependencies
    echo Please run: pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

REM Run diagnostic tests
echo Running startup diagnostics...
python test_startup.py
if errorlevel 1 (
    echo.
    echo ⚠️  Diagnostics found issues. Please review above.
    echo.
    pause
    exit /b 1
)

REM Start the application
echo.
echo Starting MedCare Application...
echo.
python main.py
