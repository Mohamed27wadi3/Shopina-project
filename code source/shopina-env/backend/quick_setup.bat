@echo off
REM Quick setup script for Shopina backend on Windows

echo ========================================
echo Shopina Backend Quick Setup
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "shopina-env" (
    echo Creating virtual environment...
    python -m venv shopina-env
    echo Virtual environment created.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call shopina-env\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Delete old database for fresh start
if exist "db.sqlite3" (
    echo Deleting old database...
    del db.sqlite3
    echo.
)

REM Run setup script
echo Running setup script...
python setup.py
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the server, run:
echo   shopina-env\Scripts\activate
echo   python manage.py runserver
echo.
pause
