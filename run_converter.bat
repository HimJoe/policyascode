@echo off
REM Quick start script for Policy-to-Code Converter (Windows)

echo Starting Policy-to-Code Converter...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Run setup_for_client.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat
echo √ Virtual environment activated
echo.

REM Run the converter
echo Launching Policy-to-Code Converter...
echo.
streamlit run policy_to_code_converter.py

REM Deactivate when done
call deactivate
