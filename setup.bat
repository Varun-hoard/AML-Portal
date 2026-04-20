@echo off
REM Quick Start Script for AML System (Windows)

echo ==========================================
echo AML System - Sprint 1 Quick Start
echo ==========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed. Please install Python 3.8 or higher.
    exit /b 1
)

echo Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if not exists
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
)

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo To start the application, run:
echo    python app.py
echo.
echo Then open your browser and go to:
echo    http://localhost:5000
echo.
echo Demo Credentials:
echo    Username: admin
echo    Password: admin123
echo.
echo ==========================================
pause
