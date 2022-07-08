import socket

HOST = "127.0.0.1"  # loopback
SERVER_PORT = 65432  # >=50_000
ADDR = (HOST, SERVER_PORT)
FORMAT = "utf8"


print("[STARTING] server is starting...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)
print(f"[LISTENING] sever is listening on {HOST} : {SERVER_PORT}")
s.listen()
print()

conn, addr = s.accept()
print(f"[SOCKET] {conn.getsockname()} is created.")
print(f"[NEW CONNECTION] {addr} connected.")

msg = conn.recv(1024).decode(FORMAT)
print(addr, ":", msg)
msg = "received: " + msg
conn.sendall(msg.encode(FORMAT))

conn.close()
