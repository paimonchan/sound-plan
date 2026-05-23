@echo off
REM Quick audio cleaning pipeline
REM Usage: drag & drop audio file onto this .bat, or run from terminal
REM clean_audio.bat input.wav

if "%~1"=="" (
    echo Usage: clean_audio.bat audio_file.wav
    echo        Drag & drop an audio file onto this script.
    pause
    exit /b
)

set VENV=E:\AI\sound-plan\.venv\Scripts
set TOOLS=E:\AI\sound-plan\tools
set INPUT=%~1
set NAME=%~n1

echo ========================================
echo Audio Cleaning Pipeline
echo Input: %INPUT%
echo ========================================
echo.

echo [1/2] Removing background music (Demucs)...
%VENV%\demucs.exe --two-stems=vocals "%INPUT%" -n htdemucs_ft
echo.

set VOCALS=separated\htdemucs\%NAME%\vocals.wav
if not exist "%VOCALS%" (
    echo Error: Demucs failed. Check input file.
    pause
    exit /b
)

echo [2/2] Removing noise (DeepFilterNet)...
%TOOLS%\deep-filter.exe "%VOCALS%" -o "%NAME%_clean.wav"
echo.

echo ========================================
echo Done! Output: %NAME%_clean.wav
echo ========================================
pause
