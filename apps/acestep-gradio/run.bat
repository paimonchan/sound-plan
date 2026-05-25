@echo off
cd /d "E:\AI\ACE-Step-1.5"

REM Add ffmpeg to PATH
set "PATH=E:\AI\ComfyUI\ffmpeg-8.1-essentials_build\bin;%PATH%"

REM Kill whatever is on port 7860 (VoxCPM2 etc.)
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":7860 "') do (
  if not "%%a"=="0" taskkill /f /pid %%a >nul 2>&1
)

echo ====================================
echo  Launching ACE-Step 1.5 Gradio UI
echo  http://localhost:7860
echo ====================================
uv run acestep --debug --port 7860
pause
