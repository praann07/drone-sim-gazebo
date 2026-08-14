import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("0.0.0.0", 9099))
s.listen(1)
s.settimeout(6.0)
print("[WSL TEST] TCP Listening on port 9099...")
try:
    conn, addr = s.accept()
    print("[WSL TEST] ACCEPTED CONNECTION FROM:", addr)
    data = conn.recv(1024)
    print("[WSL TEST] RECEIVED DATA:", data.decode("utf-8"))
    conn.close()
except Exception as e:
    print("[WSL TEST] Error:", e)
s.close()
