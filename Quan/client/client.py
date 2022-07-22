from socket import *
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
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
LOGOUT = 'Log out'
VIEW = 'View file'

client = socket(AF_INET, SOCK_STREAM)
client.connect((IP, PORT))

#Window App
window = Tk()
app_width = 720
app_height = 560

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = (screen_width/2) - (app_width/2)
y = (screen_height/2) - (app_height/2)
window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
window.title('E-NOTE')
window.iconbitmap('client/eNote.ico')
window['bg']='#DAE2B6'



# ==============================
#         FUTURE FRAMES
# ==============================
# FRAMES
# - Start screen: Sign in + Sign up + Exit program
# - Home screen (display username): New text + Upload image + Upload file + Open file + Sign out
# 
# - Sign in (signin_frame)
# - Sign up (signup_frame)
# - New text (new_text_frame)
# - Upload Image (img_frame)
# - Upload file (file_frame)
# - Open file (open_frame): View file + Download file
# - View file (view_frame)
# 
# NOTE: "home_frame" will be divided into Start screen and Home screen



# Frames
home_frame = Frame(window, padx = 2, bg= '#DAE2B6')
header_frame = Frame(window)
menu_frame = Frame(window, bg='#DAE2B6')
new_text_frame = Frame(window, bg='#DAE2B6')
img_frame = Frame(window, padx= 50, pady=50, bg= '#DAE2B6')
file_frame = Frame(window, padx= 50, pady=50, bg= '#DAE2B6')
open_frame = Frame(window, bg='#DAE2B6')
# view_frame = Frame(window)
signin_frame = Frame(window, bg='#DAE2B6')
signup_frame = Frame(window, bg='#DAE2B6')




username = ''



#Decor Home Screen










# Sign up

# Creating widgets
logup_label = Label(signup_frame, text="SIGN UP", bg='#333333', fg="#FF3399", font=("yu gothic ui", 30))
username_label = Label(signup_frame, text="Username", bg='#333333', fg="#FFFFFF", font=("yu gothic ui", 16))
new_username = Entry(signup_frame, font=("yu gothic ui", 16))
new_password = Entry(signup_frame, show="*", font=("yu gothic ui", 16))
password_label = Label(signup_frame, text="Password ", bg='#333333', fg="#FFFFFF", font=("yu gothic ui", 16))


# Placing widgets on the screen
logup_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
new_username.grid(row=1, column=1, pady=16)
password_label.grid(row=2, column=0)
new_password.grid(row=2, column=1, pady=16)
#new_username_l = Label(signup_frame, text="Username", bg='#DAE2B6')
#new_username_l.pack(fill='x', expand=True)

#new_username = Entry(signup_frame)
#new_username.pack(fill='x', expand=True)

#new_password_l = Label(signup_frame, text="Password")
#new_password_l.pack(fill='x', expand=True)

#new_password = Entry(signup_frame, show="*")
#new_password.pack(fill='x', expand=True)


def sign_up_clicked():
    if len(new_username.get()) == 0 or len(new_password.get()) == 0: messagebox.showinfo("Sign Up", "Please enter the full information.")
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
            messagebox.showwarning("Sign Up","Username must has at least 5 characters.")
        elif validation == 2:
            messagebox.showwarning("Sign Up","Password must has at least 3 characters.")
        elif validation == 3:
            messagebox.showwarning("Sign Up",f"'{new_usrname}' already existed.")
        else: 
            messagebox.showinfo("Sign Up","Registered successfully. This account can now be use to sign in.")
            new_password.delete(0, 'end')
            new_username.delete(0, 'end')


sign_up_button = Button(signup_frame, text='SIGN UP', bg="#FF3399", fg="#FFFFFF", font=("yu gothic ui", 16, 'bold'),command=sign_up_clicked)
sign_up_button.grid(row=3, column=0, columnspan=2, pady=16)


def sign_up_view():
    header_frame.pack_forget()
    home_frame.pack_forget()
    header_frame.pack(fill='x', expand=1)
    signup_frame.pack()





# Sign in

# Creating widgets
login_label = Label(signin_frame, text="LOGIN", bg='#333333', fg="#FF3399", font=("yu gothic ui", 30))
username_label = Label(signin_frame, text="Username", bg='#333333', fg="#FFFFFF", font=("yu gothic ui", 16))
signin_username = Entry(signin_frame, font=("yu gothic ui", 16))
signin_password = Entry(signin_frame, show="*", font=("yu gothic ui", 16))
password_label = Label(signin_frame, text="Password ", bg='#333333', fg="#FFFFFF", font=("yu gothic ui", 16))


# Placing widgets on the screen
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
signin_username.grid(row=1, column=1, pady=16)
password_label.grid(row=2, column=0)
signin_password.grid(row=2, column=1, pady=16)

#signin_username_l = Label(signin_frame, text="Username")
#signin_username_l.place(x= 400, y = 90)
#signin_username_l.pack(fill='x', expand=True)

#signin_username = Entry(signin_frame)
#signin_username.pack(fill='x', expand=True)

#signin_password_l = Label(signin_frame, text="Password")
#signin_password_l.pack(fill='x', expand=True)

#signin_password = Entry(signin_frame, show="*")
#signin_password.pack(fill='x', expand=True)


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
        messagebox.showinfo('NOTICE', receive_msg)
        global username

        if receive_msg == LOGIN_SUCCESS:
            username = usrname
            signin_username.delete(0, 'end')
            signin_password.delete(0, 'end')
            menu_view()


sign_in_button = Button(signin_frame, text='LOG IN', bg="#FF3399", fg="#FFFFFF", font=("yu gothic ui", 16, 'bold'),command=sign_in_clicked)
sign_in_button.grid(row=3, column=0, columnspan=2, pady=16)
#sign_in_button.pack()
      

def sign_in_view():
    header_frame.pack_forget()
    home_frame.pack_forget()
    header_frame.pack(fill='x', expand=1)
    signin_frame.pack()






# HOME

txt = "WELCOME TO"
heading = Label(header_frame, text=txt, font=('yu gothic ui', 25, "bold"), bg="#040405",fg='white', bd=5, relief=FLAT)
heading.place(x= 0, y=400)
heading.pack(fill='both', expand = True)

#header_band = Label(header_frame,bg="orange",height=2, width=150)
#header_band.grid(sticky='w')
#header_band.place(x=0,y=0)
#header_band.pack(fill=BOTH, expand=True)

e_note = Label(header_frame,text="E - NOTE",bg="black",fg="pink",font= ('verdana',33,'bold'))
e_note.place(x=1, y=400)
e_note.pack(fill='both',expand=True)
#e_note.grid(sticky='w')


signin = Button(home_frame, text="SIGN IN",bg="orange", font=('pacifico', 13, 'bold'), height= 2, width=10, relief = RIDGE, command=sign_in_view)
signin.grid(row = 15, column=0, pady = 10)

signup = Button(home_frame, text='SIGN UP',bg="orange", font=('pacifico', 13, 'bold'), height= 2,width =10, relief = RIDGE, command=sign_up_view)
signup.grid(row = 16, column=0, pady = 13)

student1 = Label(home_frame, text='21127142 - LẠC THIỆU QUÂN', fg= '#1F4690', bg = '#DAE2B6', font=('Times New Roman', 12))
student1.grid(row = 19, column = 0, pady= 11, padx= 5)
student1 = Label(home_frame, text='21127528 - NGUYỄN THỊ MINH MINH', fg= '#1F4690', bg = '#DAE2B6', font=('Times New Roman', 12))
student1.grid(row = 20, column = 0, pady= 11, padx= 5)
student1 = Label(home_frame, text='21127588 - PHẠM HOÀNG KHÁNH ĐĂNG', fg= '#1F4690', bg = '#DAE2B6', font=('Times New Roman', 12))
student1.grid(row = 21, column = 0, pady= 11, padx= 5)






# RETURN HOME

def home_view():
    header_frame.pack_forget()
    menu_frame.pack_forget()
    signin_frame.pack_forget()
    signup_frame.pack_forget()
    header_frame.pack(fill='x', expand=1)
    home_frame.pack()

back_button1 = Button(signin_frame, text=" BACK ", bg='#333333', fg="#FF3399", font=("yu gothic ui", 16, 'bold'), command=home_view)
back_button1.grid(row=4, column=0, columnspan=2, pady=10)

back_button2 = Button(signup_frame, text=" BACK ", bg='#333333', fg="#FF3399", font=("yu gothic ui", 16, 'bold'), command=home_view)
back_button2.grid(row=4, column=0, columnspan=2, pady=10)







# New text
text_box = Text(new_text_frame, height=15, width=65, font=("Consolas", 11))
text_box.insert(INSERT, "Your text here...")
text_box.pack(pady=30)

t_file_name_l = Label(new_text_frame, text='File name', font=("Consolas",12))
t_file_name_l.pack(fill='x', expand=True)
t_file_name = Entry(new_text_frame)
t_file_name.pack(fill='x', expand=True)

def save_text_clicked():
    if len(t_file_name.get()) == 0 or text_box.get('1.0', END) == '\n':
        messagebox.showerror('NOTICE','Invalid text or filename')
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
        messagebox.showinfo('NOTICE', msg)
        text_box.delete('1.0', END)
        t_file_name.delete(0, 'end')
        if msg == 'Success':
            break

save_text_button = Button(new_text_frame, text='SAVE', bg= "pink", fg="black",font=("Times New Roman",12, "bold"),command=save_text_clicked)
save_text_button.pack(anchor=E)

def new_text():
    if username == '':
        messagebox.showerror('Error', 'Login first!!!')
        return
    menu_frame.pack_forget()
    new_text_frame.pack()






# Upload image
i_file_name_l = Label(img_frame, text='File name',font= ("Times New Roman", 15))
i_file_name_l.pack(fill='x', expand=1)
i_file_name = Entry(img_frame,insertwidth=30,bg='#DAE2B6', font=("Times New Roman", 14))
i_file_name.pack(fill='x', expand=1)


def upload_img_clicked():
    if len(i_file_name.get()) == 0:
        messagebox.showerror('NOTICE','Invalid text or filename')
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
    messagebox.showinfo('NOTICE', msg)

upload_img_button = Button(img_frame, text='Save image',font=("Consolas", 14), command=upload_img_clicked)
upload_img_button.pack(fill=BOTH, expand=1)


def upload_img():
    if username == '':
        messagebox.showerror('Error', 'Login first!!!')
        return
    menu_frame.pack_forget()
    img_frame.pack()
    





# Upload file
f_file_name_l = Label(file_frame, text='File name',font= ("Times New Roman", 15))
f_file_name_l.pack(fill='x', expand=True)
f_file_name = Entry(file_frame,insertwidth=30,bg='#DAE2B6', font=("Times New Roman", 14))
f_file_name.pack(fill='x', expand=True)


def upload_file_clicked():
    if len(f_file_name.get()) == 0:
        messagebox.showerror('NOTICE','Invalid text or filename')
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

upload_file_button = Button(file_frame,text='   Save file  ',font=("Times New Roman", 14), command=upload_file_clicked)
upload_file_button.pack()

def upload_file():
    if username == '':
        messagebox.showerror('Error', 'Login first!!!')
        return
    menu_frame.pack_forget()
    file_frame.pack()






# Open file
table = ttk.Treeview(open_frame, column=('c1', 'c2'), show='headings')
table.column('#1', anchor=CENTER)
table.heading('#1', text='File name')
table.column('#2', anchor=CENTER)
table.heading('#2', text='Type')
table.pack()

# o_file_name_l = Label(open_frame, text='File name:')
# o_file_name_l.pack(pady=10, expand=True)
# o_file_name = Entry(open_frame)
# o_file_name.pack(pady=10, expand=True)

# username_label = Label(open_frame, text=username)
# username_label.pack(fill='x', expand=True)


def download_file():
    fn = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save file",
    filetypes=(("Image File", "*.jpg"), ("All Files", "*.*")))
    fn += '.' + open_file_type
    with open(ADDR+'tempFile.'+open_file_type, 'rb') as f:
        data = f.read()
    with open(fn, 'wb') as g:
        g.write(data)
    messagebox.showinfo('NOTICE', 'Download successfull')



def return_to_open_file(new_Window):
    new_Window.destroy()
    open_file()

def open_file_in_new_window(open_file_type):
    new_Window = Toplevel()
    new_Window.title('File')
    window.iconbitmap('client/eNote.ico')

    if open_file_type == 'txt':
        view_box = Text(new_Window)  # height=20, width=30 # padx=20, pady=20        
        with open(ADDR+'tempFile.txt', 'r') as f:
            view_box.insert(INSERT, f.read())
        view_box.pack()
    elif open_file_type == 'jpg' or open_file_type == 'png' or open_file_type == 'gif':
        global tk_image

        tk_image = ImageTk.PhotoImage(Image.open(ADDR+'tempFile.'+open_file_type))
        view_img = Label(new_Window, image=tk_image)
        view_img.pack()
        # view_box.image_create(END, image=tk_image)

    download_button = Button(new_Window, text='Download', command=download_file)
    download_button.pack()
    return_button = Button(new_Window, text='Exit', command=lambda: return_to_open_file(new_Window))
    return_button.pack()

def view_clicked():
    client.sendall(VIEW.encode(FORMAT))
    client.recv(1024)
    client.sendall(username.encode(FORMAT))
    client.recv(1024)


    selected = table.focus()
    if selected == '':
        messagebox.showinfo('NOTICE', 'Please choose a specific item!!!')
        return
    # open_frame.pack_forget()
    # view_frame.pack()


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

    open_file_in_new_window(open_file_type)


view_button = Button(open_frame, text='View File', font=('consolas', 14, 'bold'), command=view_clicked, bg= 'pink', fg = 'white')
view_button.pack(pady=10)

def open_file():
    if username == '':
        messagebox.showerror('Error', 'Login first!!!')
        return

    # Clear table
    for item in table.get_children():
        table.delete(item)

    menu_frame.pack_forget()
    # view_frame.pack_forget()
    open_frame.pack(expand=1)

    # view_box.delete('1.0', END)
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









# Menu

# menu = Menu(window)
# window.config(menu=menu)

# fileMenu = Menu(menu)
# fileMenu.add_command(label='New text', command=new_text)
# fileMenu.add_command(label='Upload file', command=upload_file)
# fileMenu.add_command(label='Upload image', command=upload_img)
# fileMenu.add_command(label='Open file', command=open_file)
# menu.add_cascade(label='File', menu=fileMenu)

def quit_clicked():
    files = glob.glob(ADDR+'tempFile.*')
    for f in files:
       os.remove(f)
    client.sendall(QUIT.encode(FORMAT))
    client.close()
    window.quit()

def logout():
    global username
    username = ''
    menu_frame.pack_forget()
    home_view()
    client.sendall(LOGOUT.encode(FORMAT))


# helpMenu = Menu(menu)
# helpMenu.add_command(label='Exit', command=quit_clicked)
# menu.add_cascade(label='Help', menu=helpMenu)

#Main menu
headingMENU = Label(menu_frame, text="    MENU    ", font=('yu gothic ui', 25, "bold"), bg="#040405",fg='white', bd=5, relief=FLAT)
headingMENU.grid(row=1, column=0, columnspan=3, pady=8)
newtext_button = Button(menu_frame, text = "  NEW TEXT  ", bg= "#FF7396", fg="#FFFFFF", font=("consolas", 16, 'bold'), command= new_text)
newtext_button.grid(row=2, column=0, columnspan=3, pady=10)
uploadimage_button = Button(menu_frame, text = "UPLOAD IMAGE", bg= "#FF7396", fg="#FFFFFF", font=("consolas", 16, 'bold'), command= upload_img)
uploadimage_button.grid(row=3, column=0, columnspan=3, pady=10)
uploadfile_button = Button(menu_frame, text = "UPLOAD FILE ", bg= "#FF7396", fg="#FFFFFF", font=("consolas", 16, 'bold'), command= upload_file)
uploadfile_button.grid(row=4, column=0, columnspan=3, pady=10)
openfile_button = Button(menu_frame, text = " OPEN FILE  ", bg= "#FF7396", fg="#FFFFFF", font=("consolas", 16, 'bold'), command= open_file)
openfile_button.grid(row=5, column=0, columnspan=3, pady=10)
logout_button = Button(menu_frame, text = "  LOG OUT   ", bg= "#FF7396", fg="#FFFFFF", font=("consolas", 16, 'bold'), command= logout)
logout_button.grid(row=6, column=0, columnspan=3, pady=10)
exit_button = Button(menu_frame, text = "    EXIT    ", bg= "#FF7396", fg="#FFFFFF", font=("consolas", 16, 'bold'), command= quit_clicked)
exit_button.grid(row=7, column=0, columnspan=3, pady=10)

def menu_view():
    new_text_frame.pack_forget()
    img_frame.pack_forget()
    file_frame.pack_forget()
    open_frame.pack_forget()
    signin_frame.pack_forget()
    signup_frame.pack_forget()
    header_frame.pack_forget()
    home_frame.pack_forget()
    menu_frame.pack(expand=1)

backMenu_button1 = Button(new_text_frame, text=" BACK ", bg='#333333', fg="#FF3399", font=("Consolas", 16, 'bold'),  command=menu_view)
backMenu_button1.pack()
backMenu_button2 = Button(img_frame, text=" BACK ", bg='black', fg="#FF3399", font=("Consolas", 14, 'bold'), command=menu_view)
backMenu_button2.pack()
backMenu_button3 = Button(file_frame, text=" BACK ", bg='black', fg="#FF3399", font=("Consolas", 14, 'bold'), command=menu_view)
backMenu_button3.pack()
backMenu_button4 = Button(open_frame, text=" BACK ", bg='#333333', fg="#FF3399", font=("Consolas", 16, 'bold'), command=menu_view)
backMenu_button4.pack()






# Main

def main():
    print('Waiting for server...')
    try:
        print('Connected to server')
        home_view()
        window.mainloop()
    except:
        client.close()
    finally:
        client.close()


if __name__ == '__main__':
    main()


