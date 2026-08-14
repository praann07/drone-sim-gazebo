"""
Gazebo 11 High-Speed Threaded Telemetry Bridge (Windows Host)
Streams 6-DOF drone pose (x, y, z, roll, pitch, yaw) asynchronously to Gazebo in WSL2 over TCP.
Zero UI frame-rate impact, robust background auto-reconnection.
"""

import socket
import threading
import queue
import time

class GazeboBridge:
    def __init__(self, host="127.0.0.1", port=9099):
        self.host = host
        self.port = port
        self.enabled = True
        self.last_sent = 0.0
        
        # Thread-safe telemetry queue (keeps only the most recent pose)
        self._queue = queue.Queue(maxsize=3)
        self._running = True
        self._connected = False
        
        # Start background worker thread
        self._worker_thread = threading.Thread(target=self._telemetry_worker, daemon=True)
        self._worker_thread.start()

    @property
    def is_connected(self):
        return self._connected

    def _telemetry_worker(self):
        """Dedicated background thread handling socket connection and transmission."""
        sock = None
        while self._running:
            # 1. Connect if not connected
            if sock is None:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    s.connect((self.host, self.port))
                    s.settimeout(None)
                    sock = s
                    self._connected = True
                except Exception:
                    self._connected = False
                    if sock:
                        try:
                            sock.close()
                        except Exception:
                            pass
                    sock = None
                    time.sleep(0.5)
                    continue

            # 2. Transmit queued poses
            try:
                # Wait for up to 0.1s for next pose
                msg = self._queue.get(timeout=0.1)
                sock.sendall(msg)
            except queue.Empty:
                pass
            except Exception:
                # Connection dropped
                self._connected = False
                try:
                    sock.close()
                except Exception:
                    pass
                sock = None
                time.sleep(0.2)

        if sock:
            try:
                sock.close()
            except Exception:
                pass

    def send_pose(self, drone):
        """Asynchronously dispatches the current drone pose to the transmission queue."""
        if not self.enabled:
            return
        now = drone.t
        if now - self.last_sent < 0.020:  # 50 Hz smooth streaming
            return
        self.last_sent = now

        try:
            # ENU Coordinates (+X=East, +Y=North, +Z=Altitude)
            x = float(drone.est_e)
            y = float(drone.est_n)
            z = max(0.05, float(drone.est_alt))

            # Attitudes in radians
            roll = float(drone.roll)
            pitch = float(drone.pitch)
            yaw = float(drone.yaw)

            line = f"POSE,{x:.3f},{y:.3f},{z:.3f},{roll:.4f},{pitch:.4f},{yaw:.4f}\n"
            data = line.encode("utf-8")

            # Non-blocking queue put (discard older telemetry if queue full)
            try:
                self._queue.put_nowait(data)
            except queue.Full:
                try:
                    self._queue.get_nowait()
                except queue.Empty:
                    pass
                try:
                    self._queue.put_nowait(data)
                except queue.Full:
                    pass
        except Exception:
            pass

    def close(self):
        """Clean shutdown."""
        self._running = False
