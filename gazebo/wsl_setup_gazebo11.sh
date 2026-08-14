#!/usr/bin/env bash
set -e

export PATH="$HOME/.pixi/bin:$PATH"

echo "=== 1. Checking Pixi ==="
pixi --version

echo "=== 2. Setting up dedicated Gazebo 11 Pixi Environment ==="
mkdir -p "$HOME/gazebo_env"
cd "$HOME/gazebo_env"

if [ ! -f "pixi.toml" ]; then
    pixi init .
fi

echo "=== 3. Adding Gazebo package to Pixi environment ==="
pixi add "gazebo"

echo "=== 4. Creating activation wrapper ==="
cat << 'EOF' > "$HOME/gazebo_env/run_gazebo.sh"
#!/usr/bin/env bash
set -e

# Set X11 DISPLAY routing to Windows Host VcXsrv Server
HOST_IP=$(ip route show default | awk '{print $3; exit}')
export DISPLAY="${HOST_IP}:0"
export LIBGL_ALWAYS_SOFTWARE=1
export GAZEBO_MODEL_DATABASE_URI=""

# Add custom project models to Gazebo path
PROJECT_DIR="/mnt/c/Users/karth/OneDrive/Desktop/DRONES PROJECT SIM/gazebo"
export GAZEBO_MODEL_PATH="${PROJECT_DIR}/models:${GAZEBO_MODEL_PATH}"
export GAZEBO_RESOURCE_PATH="${PROJECT_DIR}/worlds:${GAZEBO_RESOURCE_PATH}"

echo "[Gazebo 11] Connecting to X11 Display at ${DISPLAY}..."

# Execute Gazebo inside pixi environment
exec /home/tittu/.pixi/bin/pixi run --manifest-path /home/tittu/gazebo_env/pixi.toml gazebo "$@"
EOF
chmod +x "$HOME/gazebo_env/run_gazebo.sh"

echo "=== Setup Complete! ==="
