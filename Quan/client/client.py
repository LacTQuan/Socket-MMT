from socket import *
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, messagebox
import os, glob
from PIL import Image, ImageTk

IP = '127.0.0.1'
PORT = 1234
FORMAT = 'utf-8'
ADDR = 'client/'

LOGIN_SUCCESS = 'Login successfully!'
UP_FILE = 'Upload file'
UP_IMG = 'Upload img'
NEW_TEXT = 'New text'
OPEN = 'Open file'
SIGNIN = 'Sign in'
SIGNUP = 'Sign up'
QUIT = 'Quit'

client = socket(AF_INET, SOCK_STREAM)
client.connect((IP, PORT))

window = Tk()
window.geometry('720x560')


# Frames
home_frame = Frame(window)
new_text_frame = Frame(window)
img_frame = Frame(window)
file_frame = Frame(window)
open_frame = Frame(window)
view_frame = Frame(window)
signin_frame = Frame(window)
signup_frame = Frame(window)


open_file_on = False


username = ''














# Sign up
new_username_l = Label(signup_frame, text="Username")
new_username_l.pack(fill='x', expand=True)

new_username = Entry(signup_frame)
new_username.pack(fill='x', expand=True)

new_password_l = Label(signup_frame, text="Password")
new_password_l.pack(fill='x', expand=True)

new_password = Entry(signup_frame, show="*")
new_password.pack(fill='x', expand=True)


def sign_up_clicked():
    if len(new_username.get()) == 0 or len(new_password.get()) == 0: messagebox.showinfo("Thông báo", "Vui lòng nhập đầy đủ thông tin")
    else:
        client.sendall(SIGNUP.encode(FORMAT))
        client.recv(1024)
        validation = -1
        # send username and password
        new_usrname = new_username.get()
        new_psw = new_password.get()
        client.sendall(new_usrname.encode(FORMAT))
        client.recv(1024)
        client.sendall(new_psw.encode(FORMAT))
        client.recv(1024)
        # check validation
        validation = int(client.recv(1024).decode(FORMAT))
        if validation == 1:
            print("  (server) : username must has at least 5 characters.")
        elif validation == 2:
            print("  (server) : password must has at least 3 characters.")
        elif validation == 3:
            print(f"  (server) : '{new_usrname}' already existed.")
        else: 
            print("  (server) : registered successfully.")
            new_password.delete(0, 'end')
            new_username.delete(0, 'end')


sign_up_button = Button(signup_frame, text='Sign up', command=sign_up_clicked)
sign_up_button.pack()

def sign_up_view():
    new_text_frame.pack_forget()
    img_frame.pack_forget()
    file_frame.pack_forget()
    open_frame.pack_forget()
    view_frame.pack_forget()
    signin_frame.pack_forget()
    home_frame.pack_forget()
    signup_frame.pack()









# Sign in
signin_username_l = Label(signin_frame, text="Username")
signin_username_l.pack(fill='x', expand=True)

signin_username = Entry(signin_frame)
signin_username.pack(fill='x', expand=True)

signin_password_l = Label(signin_frame, text="Password")
signin_password_l.pack(fill='x', expand=True)

signin_password = Entry(signin_frame, show="*")
signin_password.pack(fill='x', expand=True)


def sign_in_clicked():
    if len(signin_username.get()) == 0 or len(signin_password.get()) == 0: messagebox.showinfo("Thông báo", "Vui lòng nhập đầy đủ thông tin")
    else:
        client.sendall(SIGNIN.encode(FORMAT))
        client.recv(1024)
        #login(client)
        
        usrname = signin_username.get()
        passwd = signin_password.get()

        #send account received to server
        client.sendall(usrname.encode(FORMAT))
        client.recv(1024)
        client.sendall(passwd.encode(FORMAT))
        client.recv(1024)

        #receive response
        receive_msg = client.recv(1024).decode(FORMAT)
        messagebox.showinfo('A', receive_msg)
        global username

        if receive_msg == LOGIN_SUCCESS:
            username = usrname
            signin_username.delete(0, 'end')
            signin_password.delete(0, 'end')


sign_in_button = Button(signin_frame, text='Sign in', command=sign_in_clicked)
sign_in_button.pack()
      

def sign_in_view():
    new_text_frame.pack_forget()
    img_frame.pack_forget()
    file_frame.pack_forget()
    open_frame.pack_forget()
    view_frame.pack_forget()
    home_frame.pack_forget()
    signup_frame.pack_forget()
    signin_frame.pack()






# HOME
signin = Button(home_frame, text="Sign in", command=sign_in_view)
signin.pack(fill='x', expand=True)
signup = Button(home_frame, text='Sign up', command=sign_up_view)
signup.pack(fill='x', expand=True)





# RETURN HOME

def back_home():
    signin_frame.pack_forget()
    signup_frame.pack_forget()
    home_frame.pack()

back_button1 = Button(signin_frame, text='Back', command=back_home)
back_button1.pack()
back_button2 = Button(signup_frame, text='Back', command=back_home)
back_button2.pack()







# New text
text_box = Text(new_text_frame, height=10, width=50)
text_box.pack()

t_file_name_l = Label(new_text_frame, text='File name')
t_file_name_l.pack(fill='x', expand=True)
t_file_name = Entry(new_text_frame)
t_file_name.pack(fill='x', expand=True)

def save_text_clicked():
    if len(t_file_name.get()) == 0 or text_box.get('1.0', END) == '\n':
        messagebox.showerror('A','Invalid text or filename')
        return
    while True:
        client.sendall(NEW_TEXT.encode(FORMAT))
        client.recv(1024)
        client.sendall(username.encode(FORMAT))
        client.recv(1024)
        data = text_box.get('1.0', 'end-1c')
        f = open(ADDR+'TextFile.txt', 'w')
        f.write(data)
        f.close()
        with open(ADDR+'TextFile.txt', 'rb') as g:
            while True:
                bytes_read = g.read(1024)
                client.sendall(str(len(bytes_read)).encode(FORMAT))
                if not bytes_read:
                    break
                client.recv(1024)
                client.sendall(bytes_read)
        os.remove(ADDR+'TextFile.txt')
        client.sendall(str(len(t_file_name.get())).encode(FORMAT))
        client.recv(1024)
        client.sendall(t_file_name.get().encode(FORMAT))
        msg = client.recv(1024).decode(FORMAT)
        messagebox.showinfo('A', msg)
        text_box.delete('1.0', END)
        t_file_name.delete(0, 'end')
        if msg == 'Success':
            break

save_text_button = Button(new_text_frame, text='Save text', command=save_text_clicked)
save_text_button.pack()    

def new_text():
    if username == '':
        messagebox.showerror('Error', 'Login first!!!')
        return
    img_frame.pack_forget()
    file_frame.pack_forget()
    open_frame.pack_forget()
    view_frame.pack_forget()
    signin_frame.pack_forget()
    signup_frame.pack_forget()
    new_text_frame.pack()
    global open_file_on
    if open_file_on:
        client.sendall('Quit open file'.encode(FORMAT))
        client.recv(1024)
    open_file_on = False






# Upload image
i_file_name_l = Label(img_frame, text='File name')
i_file_name_l.pack(fill='x', expand=True)
i_file_name = Entry(img_frame)
i_file_name.pack(fill='x', expand=True)


def upload_img_clicked():
    if len(i_file_name.get()) == 0:
        messagebox.showerror('A','Invalid text or filename')
        return
    client.sendall(UP_IMG.encode(FORMAT))
    client.recv(1024)
    client.sendall(username.encode(FORMAT))
    client.recv(1024)

    fn = filedialog.askopenfilename(title="Select file", filetypes=(("Image File", "*.jpg"), ("All Files", "*.*")))
    file_type = str(fn[fn.find('.') + 1:])
    client.sendall(str(len(file_type)).encode(FORMAT))
    client.recv(1024)
    client.sendall(file_type.encode(FORMAT))
    client.recv(1024)

    with open(fn, 'rb') as g:
        data = g.read()
        client.sendall(str(len(data)).encode(FORMAT))
        client.recv(1024)
        client.sendall(data)
        client.recv(1024)


    client.sendall(str(len(i_file_name.get())).encode(FORMAT))
    client.recv(1024)
    client.sendall(i_file_name.get().encode(FORMAT))
    msg = client.recv(1024).decode(FORMAT)
    messagebox.showinfo('A', msg)

upload_img_button = Button(img_frame, text='Save image', command=upload_img_clicked)
upload_img_button.pack()

def upload_img():
    if username == '':
        messagebox.showerror('Error', 'Login first!!!')
        return
    new_text_frame.pack_forget()
    file_frame.pack_forget()
    open_frame.pack_forget()
    view_frame.pack_forget()
    signin_frame.pack_forget()
    signup_frame.pack_forget()
    img_frame.pack()
    global open_file_on
    if open_file_on:
        client.sendall('Quit open file'.encode(FORMAT))
        client.recv(1024)
    open_file_on = False
    





# Upload file
f_file_name_l = Label(file_frame, text='File name')
f_file_name_l.pack(fill='x', expand=True)
f_file_name = Entry(file_frame)
f_file_name.pack(fill='x', expand=True)


def upload_file_clicked():
    if len(f_file_name.get()) == 0:
        messagebox.showerror('A','Invalid text or filename')
        return

    client.sendall(UP_FILE.encode(FORMAT))
    client.recv(1024)
    client.sendall(username.encode(FORMAT))
    client.recv(1024)

    fn = filedialog.askopenfilename(title='Select file', filetypes=(('Text File', '*.txt'), ('All Files', '*.*')))
    file_type = str(fn[fn.find('.') + 1:])
    client.sendall(str(len(file_type)).encode(FORMAT))
    client.recv(1024)
    client.sendall(file_type.encode(FORMAT))
    client.recv(1024)

    with open(fn, 'rb') as g:
        data = g.read()
        client.sendall(str(len(data)).encode(FORMAT))
        client.recv(1024)
        client.sendall(data)
        client.recv(1024)

    client.sendall(str(len(f_file_name.get())).encode(FORMAT))
    client.recv(1024)
    client.sendall(f_file_name.get().encode(FORMAT))
    msg = client.recv(1024).decode(FORMAT)
    messagebox.showinfo('A', msg)

upload_file_button = Button(file_frame, text='Save file', command=upload_file_clicked)
upload_file_button.pack()

def upload_file():
    if username == '':
        messagebox.showerror('Error', 'Login first!!!')
        return
    new_text_frame.pack_forget()
    img_frame.pack_forget()
    open_frame.pack_forget()
    view_frame.pack_forget()
    signin_frame.pack_forget()
    signup_frame.pack_forget()
    file_frame.pack()
    global open_file_on
    if open_file_on:
        client.sendall('Quit open file'.encode(FORMAT))
        client.recv(1024)
    open_file_on = False






# Open file
table = Treeview(open_frame, column=('c1', 'c2'), show='headings')
table.column('#1', anchor=CENTER)
table.heading('#1', text='File name')
table.column('#2', anchor=CENTER)
table.heading('#2', text='Type')
table.pack()

# o_file_name_l = Label(open_frame, text='File name:')
# o_file_name_l.pack(pady=10, expand=True)
# o_file_name = Entry(open_frame)
# o_file_name.pack(pady=10, expand=True)

username_label = Label(open_frame, text=username)
username_label.pack(fill='x', expand=True)


def download_file():
    fn = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save file",
    filetypes=(("Image File", "*.jpg"), ("All Files", "*.*")))
    fn += '.' + open_file_type
    with open(ADDR+'tempFile.'+open_file_type, 'rb') as f:
        data = f.read()
    with open(fn, 'wb') as g:
        g.write(data)
    messagebox.showinfo('A', 'Download successfull')

view_box = Text(view_frame, height=20, width=30)
view_box.pack(padx=20, pady=20)
download_button = Button(view_frame, text='Download', command=download_file)
download_button.pack(pady=10)


def view_clicked():
    selected = table.focus()
    if selected == '':
        messagebox.showinfo('A', 'Please choose a specific item!!!')
        return
    new_text_frame.pack_forget()
    img_frame.pack_forget()
    file_frame.pack_forget()
    open_frame.pack_forget()
    signin_frame.pack_forget()
    signup_frame.pack_forget()
    view_frame.pack()

    global open_file_on
    open_file_on = False

    tmp = table.item(selected, 'values')
    o_file_name = tmp[0].strip()

    client.sendall(str(len(o_file_name)).encode(FORMAT))
    client.recv(1024)
    client.sendall(o_file_name.encode(FORMAT))
    size = client.recv(1024).decode(FORMAT)
    client.sendall('OK'.encode(FORMAT))
    type = client.recv(int(size)).decode(FORMAT)
    global open_file_type
    open_file_type = type.lower()
    if open_file_type == 'text':
        open_file_type = 'txt'
    client.sendall('OK'.encode(FORMAT))
    size = client.recv(1024).decode(FORMAT)
    client.sendall('OK'.encode(FORMAT))
    data = client.recv(int(size))
    f = open(ADDR+'tempFile.'+open_file_type, 'wb')
    f.write(data)
    f.close()
    if open_file_type == 'txt':
        with open(ADDR+'tempFile.txt', 'r') as f:
            view_box.insert(INSERT, f.read())
    elif open_file_type == 'jpg' or open_file_type == 'png' or open_file_type == 'gif':
        img = Image.open(ADDR+'tempFile.'+open_file_type)
        global tk_image
        tk_image = ImageTk.PhotoImage(img)
        view_box.image_create(END, image=tk_image)


view_button = Button(open_frame, text='View', command=view_clicked)
view_button.pack(pady=10)

def open_file():
    if username == '':
        messagebox.showerror('Error', 'Login first!!!')
        return

    # Clear table
    for item in table.get_children():
        table.delete(item)

    new_text_frame.pack_forget()
    file_frame.pack_forget()
    img_frame.pack_forget()
    view_frame.pack_forget()
    signin_frame.pack_forget()
    signup_frame.pack_forget()
    open_frame.pack()
    global open_file_on
    if open_file_on:
        client.sendall('Quit open file'.encode(FORMAT))
        client.recv(1024)
    else: open_file_on = True

    view_box.delete('1.0', END)
    # o_file_name.delete(0, 'end')
    

    client.sendall(OPEN.encode(FORMAT))
    client.recv(1024)
    client.sendall(username.encode(FORMAT))
    client.recv(1024)

    client.sendall('Transfer data table...'.encode(FORMAT))

    while True:
        msg = client.recv(1024).decode(FORMAT)
        if msg == 'end':
            break
        client.sendall('OK'.encode(FORMAT))
        name = client.recv(int(msg)).decode(FORMAT)
        client.sendall('OK'.encode(FORMAT))

        msg = client.recv(1024).decode(FORMAT)
        client.sendall('OK'.encode(FORMAT))
        type = client.recv(int(msg)).decode(FORMAT)

        table.insert('', END, values=(name, type, ))


def return_to_open_file():
    os.remove(ADDR+'tempFile.'+open_file_type)
    open_file()

return_button = Button(view_frame, text='Return', command=open_file)
return_button.pack(pady=10)







# Menu
menu = Menu(window)
window.config(menu=menu)

fileMenu = Menu(menu)
fileMenu.add_command(label='New text', command=new_text)
fileMenu.add_command(label='Upload file', command=upload_file)
fileMenu.add_command(label='Upload image', command=upload_img)
fileMenu.add_command(label='Open file', command=open_file)
menu.add_cascade(label='File', menu=fileMenu)

def quit_clicked():
    files = glob.glob(ADDR+'tempFile.*')
    for f in files:
        os.remove(f)
    client.sendall(QUIT.encode(FORMAT))
    client.close()
    window.quit()

helpMenu = Menu(menu)
helpMenu.add_command(label='Exit', command=quit_clicked)
menu.add_cascade(label='Help', menu=helpMenu)







# Main

def main():
    print('Waiting for server...')
    try:
        print('Connected to server')
        home_frame.pack()
        window.mainloop()
    except:
        client.close()
    finally:
        client.close()


if __name__ == '__main__':
    main()


