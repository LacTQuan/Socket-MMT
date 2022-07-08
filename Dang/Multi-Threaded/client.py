import socket

HOST = "127.0.0.1"
PORT = 65432
ADDR = (HOST, PORT)
SIZE = 1024
FORMAT = "utf8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"[CONNECTED] client connect to server at {HOST} : {PORT}")
client.connect(ADDR)

connected = True
while connected:
    msg = input("  > ")
    client.sendall(msg.encode(FORMAT))

    if msg == "/disconnect":
        connected = False
    else:
        msg = client.recv(1024).decode(FORMAT)
        print("  (server) :", msg)
