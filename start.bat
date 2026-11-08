@echo off
title BIBI Follow Manager
cd /d "%~dp0"
python bibi_follow_manager.py
if errorlevel 1 pause
