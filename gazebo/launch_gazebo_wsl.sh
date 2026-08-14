#!/usr/bin/env bash
set -e

# WSLg Graphics Display configuration
export DISPLAY="${DISPLAY:-:0}"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-0}"
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/mnt/wslg/runtime-dir}"
export PULSE_SERVER="${PULSE_SERVER:-unix:/mnt/wslg/PulseServer}"
export LIBGL_ALWAYS_SOFTWARE=1
export GAZEBO_MODEL_DATABASE_URI=""

PROJECT_DIR="/mnt/c/Users/karth/OneDrive/Desktop/DRONES PROJECT SIM/gazebo"
export GAZEBO_MODEL_PATH="${PROJECT_DIR}/models:${GAZEBO_MODEL_PATH}"
export GAZEBO_RESOURCE_PATH="${PROJECT_DIR}/worlds:${GAZEBO_RESOURCE_PATH}"
export GAZEBO_PLUGIN_PATH="${PROJECT_DIR}/plugins:${GAZEBO_PLUGIN_PATH}"

# Clean up any previous stale Gazebo instances
killall -9 gzserver gzclient gazebo 2>/dev/null || true

echo "============================================================"
echo "🚁  STARTING GAZEBO 11 3D MISSION SIMULATOR (WSLG)"
echo "============================================================"
echo "Display Socket : ${DISPLAY}"
echo "Model Path     : ${PROJECT_DIR}/models"
echo "World Path     : ${PROJECT_DIR}/worlds/quadrotor_mission.world"
echo "Plugin Path    : ${PROJECT_DIR}/plugins/libquadrotor_pose_plugin.so"
echo "TCP Bridge     : Port 9099"
echo "============================================================"

cleanup() {
    echo -e "\n[WSL] Shutting down Gazebo simulator..."
    killall -9 gzserver gzclient gazebo 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# Launch Gazebo 11 via Pixi
/home/tittu/.pixi/bin/pixi run --manifest-path /home/tittu/gazebo_env/pixi.toml gazebo --verbose "${PROJECT_DIR}/worlds/quadrotor_mission.world"
