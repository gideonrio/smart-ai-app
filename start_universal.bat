@echo off
setlocal
title Smart AI Farm - Universal Live Link

echo ==========================================================
echo           SMART AI FARM - STARTING UNIVERSAL LINK
echo ==========================================================
echo.
echo [1/3] Closing previous app instances...
taskkill /F /IM python.exe /T >nul 2>&1

echo [2/3] Starting the Server in the background...
start /B python app.py > server_log.txt 2>&1

echo Waiting for server to initialize...
timeout /t 5 /nobreak > nul

echo [3/3] Creating Universal Global Link...
echo.
echo ==========================================================
echo 🌐 Your universal link will appear below (look for "your url is: ...")
echo 📱 Open that link on your phone.
echo ⚠️ PLEASE NOTE: When you first open the link, you will see a 
echo    "Friendly Warning" page. Click the "Click to Continue" button.
echo ==========================================================
echo.
call npx -y localtunnel --port 5000

pause
