@echo off
setlocal
title SMART AI FARM - BOOT LOADER

echo ==========================================================
echo           SMART AI FARM - SYSTEM INITIALIZATION
echo ==========================================================
echo.

:: Clean previous instances
echo [1/4] Cleaning previous sessions...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM ssh.exe /T >nul 2>&1

:: Install requirements
echo [2/4] Verifying dependencies...
pip install -r requirements.txt --quiet

:: Start Application
echo [3/4] Starting AI Engine...
start /b python app.py > server_log.txt 2>&1

:: Wait for start-up
echo.
echo Waiting 10 seconds for Neural Network to load...
timeout /t 10 /nobreak > nul

:: Start Secure Tunnel
echo [4/4] Establishing Secure Global Tunnel (Laptops/Phones)...
echo.
echo ==========================================================
echo        APP WILL BE LIVE FOR ALL DEVICES BELOW
echo ==========================================================
ssh -o StrictHostKeyChecking=no -R 80:127.0.0.1:5000 nokey@localhost.run

pause
