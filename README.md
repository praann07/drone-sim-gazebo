# 🚁 ESP32-S3 LiteWing Quadrotor Simulator & Gazebo 11 3D Digital Twin

An end-to-end drone simulation suite featuring a full 6-DOF physics engine, Voice-Activated Ground Control Station (GCS) Cockpit, Multi-Layer Satellite Mapping, and a real-time Gazebo 11 3D Digital Twin in WSLg.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Gazebo](https://img.shields.io/badge/Gazebo-11-orange)
![Pygame](https://img.shields.io/badge/Pygame-2D%20GCS-green)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 🌟 Key Features

### 1. 2D Ground Control Station (GCS) Cockpit
- **Interactive Multi-Layer Maps**: Real-world Satellite (Esri), Dark (CartoDB), Street (OSM), and Grid tiles with caching.
- **Voice Recognition Cockpit**: Speech-to-Command flight control ("Takeoff", "Land", "Start Mission", "Return Home", "Orbit", "Satellite Map").
- **Real-Time Telemetry Gauges**: 60 FPS Artificial Horizon (Attitude Indicator), Compass, Altimeter, Battery, Wind Vector, and Failsafes.
- **Autonomous Waypoint Navigation**: Auto mission trajectory execution with geofencing and automatic safety landing.

### 2. Gazebo 11 3D Digital Twin (WSLg)
- **High-Fidelity 3D Drone Model**: Custom LiteWing carbon quadrotor with ESCs, FC board, battery pack, GPS mast, and spinning props.
- **Zero-Latency In-Memory C++ Plugin**: Native `libquadrotor_pose_plugin.so` linked into `gzserver` listening on TCP port 9099.
- **3D Mission World**: Complete with a home helipad, illuminated waypoint beacons (A, B, C), and orbital camera views.
- **Asynchronous Telemetry Bridge**: Dedicated background worker thread with auto-reconnection and zero UI stutter.

---

## 🚀 Quick Start

### 1. Requirements
- **Windows 10/11** with Python 3.10+
- **WSL2 Ubuntu** with Gazebo 11 (installed via Pixi)

### 2. Python Dependencies
```bash
pip install pygame-ce SpeechRecognition pyttsx3 requests pillow
```

### 3. Run the Simulation
Launch both the Gazebo 3D World and Voice GCS Cockpit with a single command:
```powershell
.\run_gazebo_sim.bat
```

---

## 🎮 Flight Controls

### Voice Commands
| Voice Command | Action |
| :--- | :--- |
| **"Takeoff"** | Arms motors and ascends to target altitude |
| **"Start Mission"** | Initiates autonomous waypoint flight (A $\to$ B $\to$ C $\to$ Home) |
| **"Orbit"** | Enters circular point-of-interest orbit |
| **"Return Home" / "RTL"** | Flies back to launch coordinates and initiates safe landing |
| **"Land"** | Descends and disarms upon ground contact |
| **"Satellite / Dark / Street Map"** | Toggles real-time tile map layer |

### Keyboard Shortcuts
- **`Spacebar`**: Takeoff / Land
- **`M`**: Start Autonomous Mission
- **`H`**: Return to Home (RTH)
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
│   ├── dashboard.py         # 60 FPS Pygame HUD, gauges & map renderer
│   ├── map_tiles.py         # Async Web-Mercator map tile manager & cache
│   ├── physics.py           # 6-DOF Quadrotor equations of motion
│   ├── controller.py        # Cascaded PID position & attitude controllers
│   ├── navigation.py        # Waypoint trajectory planner & geofence
│   └── voice.py             # Vosk/Sphinx Speech Recognition & TTS audio
│
├── gazebo/
│   ├── models/quadrotor/    # SDF 3D LiteWing Quadrotor model
│   ├── worlds/              # 3D Mission environment & beacons
│   ├── plugins/             # Native C++ QuadrotorPosePlugin
│   ├── gazebo_client.py     # Asynchronous TCP telemetry bridge
│   └── launch_gazebo_wsl.sh # WSLg Gazebo launcher
│
└── run_gazebo_sim.bat       # 1-Click launcher for Windows + WSLg
```
