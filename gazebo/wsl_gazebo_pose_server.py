#!/usr/bin/env python3
"""
Gazebo 11 Live 6-DOF Pose Server (WSL2)
Receives 6-DOF state from Windows Controller via TCP/UDP and updates Gazebo 11 model in real-time.
"""

import json
import socket
import subprocess
import threading
import time
import sys

PORT = 9099
MODEL_NAME = "quadrotor"

latest_pose = None
pose_lock = threading.Lock()
running = True

def find_gz_bin():
    paths = [
        "/home/tittu/gazebo_env/.pixi/envs/default/bin/gz",
        "/usr/bin/gz",
        "gz"
    ]
    for p in paths:
        if subprocess.os.path.exists(p):
            return p
    return "gz"

gz_bin = find_gz_bin()

def gazebo_updater():
    global latest_pose, running, gz_bin
    last_sent = None
    
    while running:
        pose = None
        with pose_lock:
            if latest_pose is not None and latest_pose != last_sent:
                pose = dict(latest_pose)
                last_sent = dict(latest_pose)
                
        if pose is not None:
            x = pose.get("x", 0.0)
            y = pose.get("y", 0.0)
            z = max(0.05, pose.get("z", 0.05))
            roll = pose.get("roll", 0.0)
            pitch = pose.get("pitch", 0.0)
            yaw = pose.get("yaw", 0.0)
            
            cmd = [
                gz_bin,
                "model",
                "-m", MODEL_NAME,
                "-x", f"{x:.3f}",
                "-y", f"{y:.3f}",
                "-z", f"{z:.3f}",
                "-R", f"{roll:.4f}",
                "-P", f"{pitch:.4f}",
                "-Y", f"{yaw:.4f}"
            ]
            try:
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=0.15)
            except Exception:
                pass
        time.sleep(0.04)  # 25 Hz update rate

def tcp_server():
    global latest_pose, running
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        srv.bind(("0.0.0.0", PORT))
        srv.listen(2)
        print(f"[Gazebo Server] TCP Pose Bridge listening on port {PORT}...")
    except Exception as e:
        print(f"[Gazebo Server] TCP Bind Error: {e}")
        return

    while running:
        try:
            conn, addr = srv.accept()
            print(f"[Gazebo Server] Windows GCS Connected from {addr}")
            buffer = ""
            while running:
                data = conn.recv(4096)
                if not data:
                    break
                buffer += data.decode("utf-8", errors="ignore")
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if line:
                        try:
                            msg = json.loads(line)
                            with pose_lock:
                                latest_pose = msg
                        except Exception:
                            pass
            conn.close()
        except Exception:
            time.sleep(0.5)

def udp_server():
    global latest_pose, running
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind(("0.0.0.0", PORT))
    except Exception:
        return
    while running:
        try:
            data, _ = sock.recvfrom(2048)
            msg = json.loads(data.decode("utf-8"))
            with pose_lock:
                latest_pose = msg
        except Exception:
            pass

def main():
    global running
    print(f"[Gazebo Server] Starting 6-DOF Live Pose Bridge on Port {PORT}...")
    
    t_updater = threading.Thread(target=gazebo_updater, daemon=True)
    t_updater.start()
    
    t_tcp = threading.Thread(target=tcp_server, daemon=True)
    t_tcp.start()
    
    t_udp = threading.Thread(target=udp_server, daemon=True)
    t_udp.start()
    
    try:
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        running = False
        print("\n[Gazebo Server] Bridge stopped.")

if __name__ == "__main__":
    main()
