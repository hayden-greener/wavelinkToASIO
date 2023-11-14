@echo off
REM Kill existing pythonw script if running
taskkill /F /IM pythonw.exe /FI "IMAGENAME eq pythonw.exe"
SET script_dir=%~dp0
start "" pythonw "%script_dir%main.py"
