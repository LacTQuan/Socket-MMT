import socket

HOST = "127.0.0.1"
PORT = 65432
ADDR = (HOST, PORT)
SIZE = 1024
FORMAT = "utf8"

DISCONNECT_MSG = 'disconnect'
REGISTER_MSG = 'register'


def client_register(client):
    validation = -1
    while validation != 0:
        # send username and password
        print("  > REGISTER")
        username = input("    > Username: ")
        psw = input("    > Password: ")
        client.sendall(username.encode(FORMAT))
        client.recv(1024).decode(FORMAT)
        client.sendall(psw.encode(FORMAT))
        client.recv(1024).decode(FORMAT)
        # check validation
        validation = int(client.recv(1024).decode(FORMAT))
        if validation == 1:
            print("  (server) : username must has at least 5 characters.")
        if validation == 2:
            print("  (server) : password must has at least 3 characters.")
        if validation == 3:
            print(f"  (server) : '{username}' already existed.")

    print("  (server) : registered successfully.")


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"[CONNECTED] client connect to server at {HOST} : {PORT}")
    client.connect(ADDR)

    connected = True
    while connected:
        msg = input("  > ")
        client.sendall(msg.encode(FORMAT))

        if msg == DISCONNECT_MSG:
            connected = False
        elif msg == REGISTER_MSG:
            client_register(client)
        else:
            msg = client.recv(1024).decode(FORMAT)
            print("  (server) :", msg)


if __name__ == "__main__":
    main()
