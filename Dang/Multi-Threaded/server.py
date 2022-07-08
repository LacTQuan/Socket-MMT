import socket
import threading

HOST = "127.0.0.1"
PORT = 65432
ADDR = (HOST, PORT)
SIZE = 1024
FORMAT = "utf8"


def handle_client(conn, addr):
    connected = True
    while connected:
        msg = conn.recv(1024).decode(FORMAT)

        if msg == "/disconnect":
            connected = False

        print(" ", addr, ":", msg)
        msg = "received: " + msg
        conn.sendall(msg.encode(FORMAT))

    conn.close()


print("[STARTING] server is starting...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)
print(f"[LISTENING] server is listening on {HOST} : {PORT}")
s.listen()
print()

while True:
    conn, addr = s.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    print(f"[NEW CONNECTION] {addr} connected.")
