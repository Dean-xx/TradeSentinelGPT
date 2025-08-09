@echo off
REM run_windows.bat - double-click friendly runner for Windows
REM 1) Changes to this folder
cd /d "%~dp0"
REM 2) Ensure pip + requirements
python -m pip install --upgrade pip
pip install -r requirements.txt
REM 3) Run the scanner
python run.py
echo.
echo [INFO] Done. Press any key to close this window.
pause >nul