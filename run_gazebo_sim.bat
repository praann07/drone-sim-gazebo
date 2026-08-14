@echo off
cd /d "%~dp0"
title LiteWing 3D Gazebo + Voice GCS Simulator
color 0B

echo ============================================================
echo   ESP32-S3 LiteWing Quadrotor -- Gazebo 11 3D + Voice GCS
echo ============================================================
echo.

echo [1/3] Launching Gazebo 11 3D Simulation in WSL2 Ubuntu (WSLg)...
start "Gazebo 11 3D Simulation" wsl -d Ubuntu -- bash "/mnt/c/Users/karth/OneDrive/Desktop/DRONES PROJECT SIM/gazebo/launch_gazebo_wsl.sh"

echo [2/3] Waiting 4 seconds for Gazebo 3D World to initialize...
timeout /t 4 /nobreak >nul

echo.
echo [3/3] Starting Python Voice Ground Control Station Cockpit...
echo ------------------------------------------------------------
echo   Voice Commands:  "Takeoff", "Land", "Start Mission", "RTL"
echo   Keyboard Keys:   Space (Takeoff/Land), M (Mission), H (RTL)
echo   3D Navigation:   Left-Click (Orbit), Right-Click (Zoom)
echo ------------------------------------------------------------
echo.
python drone_sim\main.py

echo.
echo ============================================================
echo   Simulation closed. Cleaning up background Gazebo server...
echo ============================================================
wsl -d Ubuntu -- killall -9 gzserver gzclient gazebo 2>nul
echo Done!
pause
