@echo off
REM Kill existing pythonw script if running
taskkill /F /IM pythonw.exe /FI "IMAGENAME eq pythonw.exe"

REM Start the python script with an argument of 512
start "" pythonw "D:\GitLocal\wavelinkToASIO\main.py" 512
