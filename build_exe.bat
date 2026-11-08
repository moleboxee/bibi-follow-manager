@echo off
title Build EXE - BIBI Follow Manager
cd /d "%~dp0"
echo [1/2] Installing PyInstaller / pywebview ...
python -m pip install pyinstaller pywebview
echo [2/2] Building windowed exe ...
if exist app.ico (
  python -m PyInstaller --onefile --windowed --clean --noconfirm --name BIBI-Follow-Manager --icon app.ico --collect-all webview --add-data "app.ico;." bibi_follow_manager.py
) else (
  python -m PyInstaller --onefile --windowed --clean --noconfirm --name BIBI-Follow-Manager --collect-all webview bibi_follow_manager.py
)
echo.
echo Done! EXE at: dist\BIBI-Follow-Manager.exe  (data files saved next to the exe)
pause
