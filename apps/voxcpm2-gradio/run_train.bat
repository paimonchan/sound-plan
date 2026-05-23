@echo off
cd /d "E:\AI\sound-plan"
echo Starting VoxCPM2 Training Web UI...
echo.
call ".venv\Scripts\python.exe" "repos\VoxCPM\lora_ft_webui.py"
pause
