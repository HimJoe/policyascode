@echo off
REM Policy-to-Code Converter Setup Script for Windows

echo ================================================
echo Policy-to-Code Converter - Client Setup
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo √ Python %PYTHON_VERSION% detected
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo X Failed to create virtual environment
    pause
    exit /b 1
)

echo √ Virtual environment created
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo X Failed to install dependencies
    pause
    exit /b 1
)

echo √ Dependencies installed successfully
echo.

echo ================================================
echo √ Setup Complete!
echo ================================================
echo.
echo To run the Policy-to-Code Converter:
echo.
echo 1. Run: run_converter.bat
echo.
echo Or manually:
echo 1. Activate environment: venv\Scripts\activate
echo 2. Run converter: streamlit run policy_to_code_converter.py
echo.
echo ================================================
pause
