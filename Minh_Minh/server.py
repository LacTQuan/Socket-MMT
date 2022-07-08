import socket
import threading
import sqlite3

IP = socket.gethostbyname(socket.gethostname())
PORT = 15000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "DISCONNECT!"
LOGIN = "login"

def receive_account(conn):
    account = []
    item = None
    item = conn.recv(1024).decode(FORMAT)
    account.append(item)
    return account

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(1024).decode(FORMAT)
        if msg == DISCONNECT_MSG:
            connected = False
        if msg == LOGIN:
            msg = "START LOG IN"
            conn.sendall(msg.encode(FORMAT))
            #account_infor = receive_account(conn)
            #print("[RECEIVE: ")
            #print (account_infor)
            #checkLogin(conn)
            usr_account = conn.recv(1024).decode(FORMAT)
            pass_account = conn.recv(1024).decode(FORMAT)
            con = sqlite3.connect('login.db')
            cur = con.cursor()
            cur.execute(f"SELECT password FROM login WHERE username = ?", (usr_account,))
    
            if(pass_account, ) in cur.fetchall():
                print("LOGIN SUCCESSFULLY!")
                conn.sendall(("LOGIN SUCCESSFULLY!").encode(FORMAT))
            else:
                print("LOGIN UNSUCCESSFULLY!")
                conn.sendall(("USERNAME OR PASSWORD ARE INCORRECT.").encode(FORMAT))
        else:
            print(f"[{addr}] {msg}")
            msg = f"Msg received: {msg}"
            conn.sendall(msg.encode(FORMAT))
            
                   
    conn.close()


def start():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args= (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

if __name__ == "__main__":
    start()
