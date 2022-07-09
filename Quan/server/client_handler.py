FORMAT = 'utf-8'
ADDR = 'server/'


# Sign up

def validate_account(username, psw, cur):
    # CHECK IF USERNAME OR PASSWORD IS TOO SHORT
    if len(username) < 5:
        return 1
    if len(psw) < 3:
        return 2

    # CHECK IF USERNAME ALREADY EXIST

    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    # If username already exist
    if cur.fetchone():
        return 3
    # If username is valid
    cur.execute("INSERT INTO users VALUES (?, ?)", (username, psw))

    return 0


def client_register(conn, cur):
    conn.sendall('OK'.encode(FORMAT))
    validation = -1
    # receive username and password
    username = conn.recv(1024).decode(FORMAT)
    conn.sendall(username.encode(FORMAT))
    psw = conn.recv(1024).decode(FORMAT)
    conn.sendall(psw.encode(FORMAT))
    # check validation
    validation = validate_account(username, psw, cur)
    conn.sendall(str(validation).encode(FORMAT))




# Sign in
def check_logged_in_accout(cur_user, usr_account):
    return usr_account in cur_user

def client_signin(conn, cur, cur_user):
    conn.sendall('OK'.encode(FORMAT))

    usr_account = conn.recv(1024).decode(FORMAT)
    conn.sendall('OK'.encode(FORMAT))
    pass_account = conn.recv(1024).decode(FORMAT)
    conn.sendall('OK'.encode(FORMAT))

    # check account
    cur.execute(f"SELECT password FROM users WHERE username = ?", (usr_account,))

    if(pass_account, ) in cur.fetchall():
        if check_logged_in_accout(cur_user, usr_account):
            conn.sendall('Invalid!'.encode(FORMAT))
        else:
            cur_user.append(usr_account)
            conn.sendall(("Login successfully!").encode(FORMAT))
            return usr_account
    else:
        conn.sendall(("Username or password are incorrect.").encode(FORMAT))
    return ''






def new_text(cur, conn, os):
    conn.sendall('OK'.encode(FORMAT))
    username = conn.recv(1024).decode(FORMAT)
    conn.sendall('OK'.encode(FORMAT))
    with open(ADDR+'TextFile.txt', 'wb') as f:
        while True:
            size = conn.recv(1024).decode(FORMAT)
            if size == '0':
                break
            conn.sendall('OK'.encode(FORMAT))
            bytes_read = conn.recv(int(size))
            f.write(bytes_read)
    data = b''
    with open(ADDR+'TextFile.txt', 'rb') as g:
        while True:
            bytes_read = g.read(1024)
            if not bytes_read:
                break
            data += bytes_read
    os.remove(ADDR+'TextFile.txt')
    size = conn.recv(1024).decode(FORMAT)
    conn.sendall('OK'.encode(FORMAT))
    file_name = conn.recv(int(size)).decode(FORMAT)
    try:
        query = 'INSERT INTO files (username, file_name, type, contents) VALUES (?, ?, ?, ?)'
        cur.execute(query, (username, username+'_'+file_name, 'text', data, ))
        conn.sendall('Success'.encode(FORMAT))
    except:
        conn.sendall('Something went wrong :((('.encode(FORMAT))

# https://youtu.be/NwvTh-gkdfs


def upload_image(cur, conn, os):
    conn.sendall('OK'.encode(FORMAT))
    username = conn.recv(1024).decode(FORMAT)
    conn.sendall('OK'.encode(FORMAT))

    size = conn.recv(1024).decode(FORMAT)
    conn.sendall('OK'.encode(FORMAT))
    file_type = conn.recv(int(size)).decode(FORMAT)
    conn.sendall('OK'.encode(FORMAT))

    with open(ADDR+'ImgFile.'+file_type, 'wb') as f:
        size = conn.recv(1024).decode(FORMAT)
        conn.sendall('OK'.encode(FORMAT))
        data = conn.recv(int(size))
        conn.sendall('OK'.encode(FORMAT))
        f.write(data)
        f.close()


    size = conn.recv(1024).decode(FORMAT)
    conn.sendall('OK'.encode(FORMAT))
    file_name = conn.recv(int(size)).decode(FORMAT)

    with open(ADDR+'ImgFile.'+file_type, 'rb') as f:
        data = f.read()
    os.remove(ADDR+'ImgFile.'+file_type)
    try:
        query = 'INSERT INTO files (username, file_name, type, contents) VALUES (?, ?, ?, ?)'
        cur.execute(query, (username, username+'_'+file_name, file_type, data, ))
        conn.sendall('Success'.encode(FORMAT))
    except:
        conn.sendall('Something went wrong :((('.encode(FORMAT))


def upload_file(cur, conn, os):
    conn.sendall('OK'.encode(FORMAT))
    username = conn.recv(1024).decode(FORMAT)
    conn.sendall('OK'.encode(FORMAT))

    size = conn.recv(1024).decode(FORMAT)
    conn.sendall('OK'.encode(FORMAT))
    file_type = conn.recv(int(size)).decode(FORMAT)
    conn.sendall('OK'.encode(FORMAT))

    with open(ADDR+'File.'+file_type, 'wb') as f:
        size = conn.recv(1024).decode(FORMAT)
        conn.sendall('OK'.encode(FORMAT))
        data = conn.recv(int(size))
        conn.sendall('OK'.encode(FORMAT))
        f.write(data)
        f.close()

    size = conn.recv(1024).decode(FORMAT)
    conn.sendall('OK'.encode(FORMAT))
    file_name = conn.recv(int(size)).decode(FORMAT)

    with open(ADDR+'File.'+file_type, 'rb') as f:
        data = f.read()
    os.remove(ADDR+'File.'+file_type)
    try:
        query = 'INSERT INTO files (username, file_name, type, contents) VALUES (?, ?, ?, ?)'
        cur.execute(query, (username, username+'_'+file_name, file_type, data, ))
        conn.sendall('Success'.encode(FORMAT))
    except:
        conn.sendall('Something went wrong :((('.encode(FORMAT))



def open_file(cur, conn):
    conn.sendall('OK'.encode(FORMAT))
    username = conn.recv(1024).decode(FORMAT)
    conn.sendall('OK'.encode(FORMAT))

    conn.recv(1024)

    query = 'SELECT * FROM files WHERE username=?'
    cur.execute(query, (username, ))
    rows = cur.fetchall()
    for row in rows:
        name = str(row[1][row[1].find('_')+1:])
        conn.sendall(str(len(name)).encode(FORMAT))
        conn.recv(1024)
        conn.sendall(name.encode(FORMAT))
        conn.recv(1024)

        file_type = str(row[2])
        conn.sendall(str(len(file_type)).encode(FORMAT))
        conn.recv(1024)
        conn.sendall(file_type.encode(FORMAT))

    conn.sendall('end'.encode(FORMAT))

    size = conn.recv(1024).decode(FORMAT)
    conn.sendall('OK'.encode(FORMAT))
    if size == 'Quit open file':
        return
    file_name = conn.recv(int(size)).decode(FORMAT)

    cur.execute('SELECT * FROM files WHERE file_name=? LIMIT 1', (username+'_'+file_name, ))
    result = cur.fetchone()
    type = result[2]
    conn.sendall(str(len(type)).encode(FORMAT))
    conn.recv(1024)
    conn.sendall(type.encode(FORMAT))
    conn.recv(1024)
    data = result[3]
    conn.sendall(str(len(data)).encode(FORMAT))
    conn.recv(1024)
    conn.sendall(data)
