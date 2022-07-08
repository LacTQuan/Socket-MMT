import socket

HOST = "127.0.0.1"
PORT = 65432
ADDR = (HOST, PORT)
FORMAT = "utf8"


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print(f"[CONNECTED] client connect to server at {HOST} : {PORT}")
client.connect(ADDR)

# Client chat first
msg = input("  > ")
client.sendall(msg.encode(FORMAT))

connected = True
while connected:
    msg = client.recv(1024).decode(FORMAT)

    if msg == "/ DISCONNECT":
        connected = False
        msg = "/ DISCONNECT"
        client.sendall(msg.encode(FORMAT))
    else:
        print("  (server) :", msg)
        msg = input("  > ")
        client.sendall(msg.encode(FORMAT))
