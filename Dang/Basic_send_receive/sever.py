import socket

HOST = "127.0.0.1"
PORT = 65432
ADDR = (HOST, PORT)
FORMAT = "utf8"


print("[STARTING] server is starting...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)
print(f"[LISTENING] server is listening on {HOST} : {PORT}")
s.listen()
print()

conn, addr = s.accept()
print(f"[SOCKET] {conn.getsockname()} is created.")
print(f"[NEW CONNECTION] {addr} connected.")

connected = True
while connected:
    msg = conn.recv(1024).decode(FORMAT)

    if msg == "/ DISCONNECT":
        connected = False
        msg = "/ DISCONNECT"
        conn.sendall(msg.encode(FORMAT))
    else:
        print(" ", addr, ":", msg)
        msg = input("  > ")
        conn.sendall(msg.encode(FORMAT))

conn.close()
