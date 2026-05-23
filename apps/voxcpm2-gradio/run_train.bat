@echo off
cd /d "E:\AI\sound-plan"
echo Stopping any running Gradio on port 7860...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :7860') do taskkill /F /PID %%a 2>nul
echo.
echo Starting VoxCPM2 Training Web UI...
echo.
set PYTHONPATH=E:\AI\sound-plan\repos\VoxCPM\src
call ".venv\Scripts\python.exe" "repos\VoxCPM\lora_ft_webui.py"
pause
