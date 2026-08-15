@echo off
cd /d "%~dp0"
title LiteWing Drone GCS Cockpit Simulator
color 0A

echo ============================================================
echo   ESP32-S3 LiteWing Quadrotor -- Python Voice GCS Simulator
echo ============================================================
echo.
echo   [Controls Summary]
echo   ----------------------------------------------------------
echo   Voice Commands : "Takeoff", "Land", "Start Mission", "Orbit", "RTL"
echo   Spacebar       : Takeoff / Land Toggle
echo   M Key          : Start Autonomous Waypoint Mission
echo   H Key          : Return to Home (RTL)
echo   K Key          : Switch Map Layer (Satellite / Dark / OSM / Grid)
echo   W / S          : Manual Pitch Forward / Backward
echo   A / D          : Manual Roll Left / Right
echo   Up / Down      : Manual Altitude Ascend / Descend
echo   Left / Right   : Manual Yaw Rotate Left / Right
echo   ----------------------------------------------------------
echo.
echo Launching GCS Cockpit...
python drone_sim\main.py

echo.
pause
