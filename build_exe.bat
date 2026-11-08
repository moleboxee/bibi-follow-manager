@echo off
title Build EXE - BIBI Follow Manager
cd /d "%~dp0"
echo [1/2] Installing PyInstaller ...
python -m pip install pyinstaller
echo [2/2] Building exe ...
if exist app.ico (
  python -m PyInstaller --onefile --clean --noconfirm --name BIBI-Follow-Manager --icon app.ico bibi_follow_manager.py
) else (
  python -m PyInstaller --onefile --clean --noconfirm --name BIBI-Follow-Manager bibi_follow_manager.py
)
echo.
echo Done! EXE at: dist\BIBI-Follow-Manager.exe
pause
