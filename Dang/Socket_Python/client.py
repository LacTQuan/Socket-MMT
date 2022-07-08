import socket

HOST = "127.0.0.1"  # loopback
SERVER_PORT = 65432  # >=50_000
ADDR = (HOST, SERVER_PORT)
FORMAT = "utf8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"[CONNECTED] client connect to server at {HOST} : {SERVER_PORT}")
client.connect(ADDR)

msg = input("> ")
client.sendall(msg.encode(FORMAT))
msg = client.recv(1024).decode(FORMAT)
print("(server) :", msg)
