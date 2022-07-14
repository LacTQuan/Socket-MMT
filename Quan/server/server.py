from socket import *
import threading
import sqlite3
from client_handler import *
import os

IP = '127.0.0.1'
PORT = 1234
FORMAT = 'utf-8'
ADDR = 'server/'

UP_FILE = 'Upload file'
UP_IMG = 'Upload img'
NEW_TEXT = 'New text'
OPEN = 'Open file'
SIGNIN = 'Sign in'
SIGNUP = 'Sign up'
QUIT = 'Quit'
LOGOUT = 'Log out'
VIEW = 'View file'


server = socket(AF_INET, SOCK_STREAM)

cur_user = []

def Exit(conn, addr, username):
    conn.close()
    if username != '':
        cur_user.remove(username)
    print(f'{addr[0]} : {addr[1]} disconnected')

def client_handler(conn, addr):
    mydb = sqlite3.connect(ADDR+'data.db')
    cur = mydb.cursor()
    username = ''
    while True:
        choice = conn.recv(1024).decode(FORMAT)
        if choice == NEW_TEXT:
            new_text(cur, conn, os)
            mydb.commit()
        elif choice == UP_IMG:
            upload_image(cur, conn, os)
            mydb.commit()
        elif choice == UP_FILE:
            upload_file(cur, conn, os)
            mydb.commit()
        elif choice == OPEN:
            open_file(cur, conn)
        elif choice == SIGNIN:
            username = client_signin(conn, cur, cur_user)
        elif choice == SIGNUP:
            client_register(conn, cur)
            mydb.commit()
        elif choice == QUIT:
            Exit(conn, addr, username)
            break
        elif choice == LOGOUT:
            cur_user.remove(username)
            username = ''
        elif choice == VIEW:
            view_file(cur, conn)
    


def accept_connections():
    conn, addr = server.accept()
    thread = threading.Thread(target = client_handler, args= (conn, addr))
    thread.start()
    print(f'Connected to {addr[0]} : {str(addr[1])}')
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


def start_server():
    print("[STARTING] Server is starting...")
    server.bind((IP, PORT))
    server.listen(5)
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    try:
        while True:
            accept_connections()
    except KeyboardInterrupt:
        server.close()
    finally:
        server.close()

def main():
    start_server()

if __name__ == '__main__':
    main()
