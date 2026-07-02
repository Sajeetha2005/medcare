@echo off
REM Absolute minimal startup test
REM This tries to start the app and show any errors

echo.
echo Testing MedCare startup...
echo.

python app_simple.py

echo.
if errorlevel 1 (
    echo Application failed. Checking installation...
    echo.
    echo Checking Python:
    python --version
    echo.
    echo Checking Flask:
    pip show flask 2>nul || echo ✗ Flask NOT installed - run: pip install flask
    echo.
    echo Checking pandas:
    pip show pandas 2>nul || echo ✗ pandas NOT installed - run: pip install pandas
    echo.
    echo Checking joblib:
    pip show joblib 2>nul || echo ✗ joblib NOT installed - run: pip install joblib
    echo.
    echo Full diagnostics:
    echo python test_startup.py
    echo.
)

pause
