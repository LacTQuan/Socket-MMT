import socket


IP = socket.gethostbyname(socket.gethostname())
PORT = 15000
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
LOGIN = "login"

DISCONNECT_MSG = "DISCONNECT!"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    print(f"[CONNECTED] Client connected to server at {IP} : {PORT}")

    connected = True
    while connected:
        msg = input("CHAT> ")

        client.sendall(msg.encode(FORMAT))

        if msg == DISCONNECT_MSG:
            connected = False
        if msg == LOGIN:
            client.recv(1024).decode(FORMAT)
            #login(client)
            
            usrname = input('username: ')
            passwd = input('password: ')

            #send account received to server
            client.sendall(usrname.encode(FORMAT))
            client.sendall(passwd.encode(FORMAT))
    
            #receive response
            receive_msg = client.recv(1024).decode(FORMAT)
            print(receive_msg)
        else:
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER] {msg}")
        

def login(client):
    valid_account = []
    usrname = input('username: ')
    passwd = input('password: ')

    valid_account.append(usrname)
    valid_account.append(passwd)

    #send account received to server
    for item in valid_account:
        client.sendall(item.encode(FORMAT))
        #client.recv(1024)

    #receive response
    receive_msg = client.recv(1024).decode(FORMAT)
    print(receive_msg)


if __name__ == "__main__":
    main()