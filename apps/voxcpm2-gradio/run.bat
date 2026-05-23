@echo off
cd /d "E:\AI\sound-plan"
echo Starting VoxCPM2 Gradio Web UI...
echo.
call ".venv\Scripts\python.exe" "apps\voxcpm2-gradio\app.py"
pause
