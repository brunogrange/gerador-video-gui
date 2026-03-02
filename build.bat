@echo off
echo.
echo ==========================================
echo   Slideshow Pro Maker - Build Script
echo ==========================================
echo.

echo Checking for PyInstaller...
python -m PyInstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] PyInstaller not found.
    echo Please run: pip install pyinstaller
    pause
    exit /b %errorlevel%
)

echo.
echo Building executable...
python -m PyInstaller --noconsole --onefile gerador_video_gui.py

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo   BUILD SUCCESSFUL!
    echo   Executable located in the 'dist' folder.
    echo.
    echo   IMPORTANT: Remember to copy 'ffmpeg.exe'
    echo   to the 'dist' folder for audio support.
    echo ==========================================
) else (
    echo.
    echo [ERROR] Build failed.
    pause
)

echo.
pause
