import socket
import threading
import time

TARGET_HOST = "127.0.0.1"
TARGET_PORT = 7632
CONNECTIONS = 50

def worker(client_id):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TARGET_HOST, TARGET_PORT))
        s.send(f"/login TestUser{client_id} TestPass".encode())
        time.sleep(1)
        s.close()
    except Exception as e:
        print(f"Client {client_id} error:", e)

threads = []
for i in range(CONNECTIONS):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"{CONNECTIONS} connections tested.")