# 🚁 ESP32-S3 LiteWing Quadrotor Voice GCS Simulator & Autopilot

An end-to-end drone simulation and ground control station featuring a full 6-DOF physics engine, Voice-Activated Ground Control Station (GCS) Cockpit, Multi-Layer Satellite Mapping, and interactive waypoint mission autonomy for ESP32 / ESP32-S3 drones.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Pygame](https://img.shields.io/badge/Pygame-2D%20GCS-green)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 🌟 Key Features

### 1. 2D Ground Control Station (GCS) Cockpit
- **Interactive Multi-Layer Maps**: Real-world Satellite (Esri), Dark (CartoDB), Street (OSM), and Topographic Grid tiles with caching.
- **Voice Recognition Cockpit**: Speech-to-Command flight control ("Takeoff", "Land", "Start Mission", "Return Home", "Orbit", "Satellite Map", "Hover at P1").
- **Real-Time Telemetry Gauges**: 60 FPS Artificial Horizon (Attitude Indicator), Heading Compass, Altimeter, Battery Voltage, Wind Vector, and Failsafes.
- **Interactive Waypoint Autonomy**: Click to add custom waypoints (`P1`, `P2`, etc.), select points for instant **Fly To**, **Hover**, **Orbit**, or **Delete** actions.
- **Failsafe & Geofencing**: Automatic Return to Home (RTH) on critical battery, link timeout, or geofence boundary breach.

---

## 🚀 Quick Start

### 1. Requirements
- **Windows 10/11** with Python 3.10+
- Dependencies:
```bash
pip install pygame-ce SpeechRecognition pyttsx3 requests pillow
```

### 2. Run the Simulator
Launch the simulation with a single click or command:
```powershell
.\run_sim.bat
```

---

## 🎮 Controls Summary

### Interactive Mouse Actions
- **Click Map (Empty Area)**: Add a new custom waypoint (`P1`, `P2`, ...) and fly there.
- **Click Existing Waypoint**: Pops up the interactive **Waypoint Action Card** (`[ FLY TO ]`, `[ HOVER ]`, `[ ORBIT ]`, `[ DELETE ]`).
- **Scroll Wheel**: Smooth zoom in / zoom out.

### Voice Commands
| Voice Command | Action |
| :--- | :--- |
| **"Takeoff"** | Arms motors and ascends to target altitude |
| **"Start Mission"** | Initiates autonomous waypoint flight |
| **"Orbit" / "Orbit P1"** | Enters circular point-of-interest orbit |
| **"Stop Orbit" / "Cancel Orbit"** | Exits orbit mode and holds steady in Hover |
| **"Hover at P1"** | Flies to `P1` and locks position in hover |
| **"Delete P1"** | Removes custom waypoint `P1` |
| **"Return Home" / "RTL"** | Flies back to launch coordinates and lands safely |
| **"Land"** | Descends and disarms upon touchdown |
| **"Satellite / Dark / Street Map"** | Toggles real-time tile map layer |

### Keyboard Shortcuts
- **`Spacebar`**: Takeoff / Land toggle
- **`M`**: Start Autonomous Mission
- **`P`**: Pause / Hover / Position Hold
- **`O`**: Toggle POI Orbit Mode (Start / Stop)
- **`H` / `R`**: Return to Home (RTL)
- **`K`**: Cycle Map Layer (Satellite $\to$ Dark $\to$ Street $\to$ Grid)
- **`W` / `S`**: Manual Pitch Forward / Backward
- **`A` / `D`**: Manual Roll Left / Right
- **`Up` / `Down` Arrow**: Ascend / Descend
- **`Left` / `Right` Arrow**: Yaw Rotate Left / Right

---

## 📁 Project Architecture

```
├── drone_sim/
│   ├── main.py              # Main application entry point & event loop
│   ├── dashboard.py         # 60 FPS Pygame HUD, gauges, interactive map & action cards
│   ├── map_tiles.py         # Async Web-Mercator map tile manager & disk cache
│   ├── physics.py           # 6-DOF Quadrotor equations of motion
│   ├── controller.py        # Cascaded PID position & attitude controllers
│   ├── navigation.py        # Waypoint trajectory planner & geofence
│   ├── commands.py          # Voice command regex parser & intent extractor
│   └── voice.py             # Vosk/Sphinx Speech Recognition & TTS audio
│
└── run_sim.bat              # 1-Click native Windows launcher
```
