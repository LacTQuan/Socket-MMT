import socket
import threading
import sqlite3

HOST = "127.0.0.1"
PORT = 65432
ADDR = (HOST, PORT)
SIZE = 1024
FORMAT = "utf8"

DISCONNECT_MSG = 'disconnect'
REGISTER_MSG = 'register'


def validate_account(username, psw):
    # CHECK IF USERNAME OR PASSWORD IS TOO SHORT
    if len(username) < 5:
        return 1
    if len(psw) < 3:
        return 2

    # CHECK IF USERNAME ALREADY EXIST
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    # If username already exist
    if c.fetchone():
        conn.close()
        return 3
    # If username is valid
    c.execute("INSERT INTO users VALUES (?, ?)", (username, psw))
    conn.commit()
    conn.close()

    return 0


def client_register(conn, addr):
    validation = -1
    while validation != 0:
        # receive username and password
        username = conn.recv(1024).decode(FORMAT)
        conn.sendall(username.encode(FORMAT))
        psw = conn.recv(1024).decode(FORMAT)
        conn.sendall(psw.encode(FORMAT))
        # check validation
        validation = validate_account(username, psw)
        if validation == 1:
            conn.sendall(str(validation).encode(FORMAT))
        if validation == 2:
            conn.sendall(str(validation).encode(FORMAT))
        if validation == 3:
            conn.sendall(str(validation).encode(FORMAT))

    conn.sendall(str(validation).encode(FORMAT))


def handle_client(conn, addr):
    connected = True
    while connected:
        msg = conn.recv(1024).decode(FORMAT)

        if msg == DISCONNECT_MSG:
            connected = False
            print(f"[DISCONNECTION] {addr} disconnected.")
        elif msg == REGISTER_MSG:
            client_register(conn, addr)
            print(f"[REGISTER] {addr} registered.")
        else:
            msg = "cannot recognize the command."
            conn.sendall(msg.encode(FORMAT))

    conn.close()


def main():
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


if __name__ == "__main__":
    main()
