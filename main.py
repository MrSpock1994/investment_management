import smtplib, ssl
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import random
import string
from matplotlib.pyplot import text
import pandas as pd
from hashlib import sha256

root = Tk()
root.title("Login")
root.geometry("245x310")
style = ttk.Style(root)



def login():
    global logged_as 
    logged_as = username.get()
    login_screen = Tk()
    login_screen.title("Logged as " + logged_as )
    login_screen.geometry("1500x1000")
    button_cripto = ttk.Button(login_screen, text="CRIPTOS", command=cripto)
    button_cripto.place(x=170, y=40, width=300, height=120)
    button_cripto = ttk.Button(login_screen, text="STOKS", command=stoks)
    button_cripto.place(x=630, y=40, width=300, height=120)
    button_cripto = ttk.Button(login_screen, text="SAVINGS", command=savings)
    button_cripto.place(x=1080, y=40, width=300, height=120)
    root.destroy()


def cripto():
    return


def stoks():
    return


def savings():
    return


def hash_password(initial_password):
    global encrypted_password
    encrypt_first = initial_password.encode('utf-8')
    h = sha256()
    h.update(encrypt_first)
    hashed = h.hexdigest()
    encrypted_password = hashed[:4] + "!" + hashed[10:16] + "&" + hashed[25:36] + "B"


def check_login():
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT *, oid FROM users WHERE username = ?", (username.get(),))
    check_login_base = cursor.fetchall()
    hash_password(password.get())
    if len(check_login_base) == 0:
        messagebox.showinfo("User not found","Please check the username.")
    if (len(check_login_base) > 0) and (check_login_base[0][3] != encrypted_password):
        messagebox.showinfo("Credentials not valid","Please check the password.")
    if len(check_login_base) > 0 and check_login_base[0][3] == encrypted_password:
        login()


def forgot_password():
    global reset_password
    global reset_code
    forgot_password_screen = Tk()
    forgot_password_screen.title("Forgot password")
    forgot_password_screen.geometry("290x310")
    reset_password = ttk.Entry(forgot_password_screen, width=30)
    reset_password.insert(END, "Your email")
    reset_password.place(x=20, y=40)
    reset_code = ttk.Entry(forgot_password_screen, width=30)
    reset_code.insert(END, "Enter the code")
    reset_code.place(x=20, y=80)
    button_reset_code= ttk.Button(forgot_password_screen, text="Send code", command=code_reset_password)
    button_reset_code.place(x=100, y=120)
    button_reset_password= ttk.Button(forgot_password_screen, text="Reset", command=confirm_forgot_password)
    button_reset_password.place(x=100, y=160)


def confirm_forgot_password():
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT *, oid FROM users WHERE email = ?", (reset_password.get(),))
    check_email_exists = cursor.fetchall()
    #check if email belongs to a existing register
    if len(check_email_exists) == 0:
        messagebox.showinfo("Email not found","Email not registered\nplease check.")
    #check if the code is correct
    if len(check_email_exists) >= 1 and reset_code.get() != final_new_code_generate:
        messagebox.showinfo("Wrong code","You entered a wrong code\nplease check.")
    #generate new password, hashed it and update the database
    if len(check_email_exists) >= 1 and reset_code.get() == final_new_code_generate:
        letters = list(string.ascii_letters + string.digits)
        random.shuffle(letters)
        #setting the lenght of the new password to 10 letters
        new_password_generate = []
        for i in range(0, 10, 1):
            new_password_generate.append(random.choice(letters))
        #converting it to a string and hashing it
        final_new_password_generate = "".join(new_password_generate)
        hash_password(final_new_password_generate)
        cursor.execute("UPDATE users SET name = ?, username = ?, email = ?, password = ?"
                   "WHERE oid = ?",
                    [check_email_exists[0][0], check_email_exists[0][1], check_email_exists[0][2], encrypted_password, check_email_exists[0][4]])
        conn.commit()
        conn.close()
            

def code_reset_password():
    global final_new_code_generate
    #send and email with the code to reset_password.get()
    code = list(string.ascii_letters + string.digits)
    random.shuffle(code)
    #setting the lenght of the new code to 6 letters
    new_code = []
    for i in range(0, 6, 1):
        new_code.append(random.choice(code))
    final_new_code_generate = "".join(new_code)
    #messagebox.showinfo(new_code)

        
def register_one():
    global register_name
    global register_username
    global register_email
    global register_password
    global register_password_confirm
    register_screen = Tk()
    register_screen.title("Register new user")
    register_screen.geometry("290x310")
    register_namelabel = ttk.Label(register_screen, text="Your Full name")
    register_namelabel.place(x=20, y=20)
    register_name = ttk.Entry(register_screen, width=30)
    register_name.place(x=20, y=40)
    register_usernamelabel = ttk.Label(register_screen, text="Choose a username")
    register_usernamelabel.place(x=20, y=60)
    register_username = ttk.Entry(register_screen, width=30)
    register_username.place(x=20, y=80)
    register_emaillabel = ttk.Label(register_screen, text="Insert your email")
    register_emaillabel.place(x=20, y=100)
    register_email = ttk.Entry(register_screen, width=30)
    register_email.place(x=20, y=120)
    register_passwordlabel = ttk.Label(register_screen, text="Create a password")
    register_passwordlabel.place(x=20, y=140)
    register_password = ttk.Entry(register_screen, show='*', width=30)
    register_password.place(x=20, y=160)
    register_password_confirmlabel = ttk.Label(register_screen, text="Confirm the password")
    register_password_confirmlabel.place(x=20, y=180)
    register_password_confirm = ttk.Entry(register_screen, show='*', width=30)
    register_password_confirm.place(x=20, y=200)
    button_confirm_register = ttk.Button(register_screen, text="Confirm", command=register_two)
    button_confirm_register.place(x=100, y=240)
   

def register_two():
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()
    #checks if passwords are equal
    if register_password.get() != register_password_confirm.get():
        messagebox.showinfo("Password not equal","The passwords does not match\nplease check.")
    #check if the email is already in use
    cursor.execute("SELECT *, oid FROM users WHERE email = ?", (register_email.get(),))
    check_email = cursor.fetchall()
    if len(check_email) >= 1:
        messagebox.showinfo("Email not avaiable","This email is already in use\nplease check.")
    #check if the username is already in use
    cursor.execute("SELECT *, oid FROM users WHERE username = ?", (register_username.get(),))
    check_username = cursor.fetchall()
    if len(check_username) >= 1:
        messagebox.showinfo("Username not avaiable","This username is already in use\nplease check.")
    if len(check_email) == 0 and len(check_username) == 0 and register_password.get() == register_password_confirm.get():
        hash_password(register_password.get())
        insert_user = [register_name.get(), register_username.get(), register_email.get(), encrypted_password]
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?)", insert_user)
        messagebox.showinfo("Registered!","Sucessfully registered\nYou may now login.")
    conn.commit()
    conn.close()

usernamelabel = ttk.Label(root, text="Username")
usernamelabel.place(x=85, y=20)
username = ttk.Entry(root, width=20)
username.place(x=40, y=40)
passwordlabel = ttk.Label(root, text="Password")
passwordlabel.place(x=85, y=60)
password = ttk.Entry(root, show='*', width=20)
password.place(x=40, y=80)
button_login = ttk.Button(root, text="Login", command=check_login)
button_login.place(x=80, y=120)
button_register = ttk.Button(root, text="Register", command=register_one)
button_register.place(x=80, y=160)
button_forgot_pass = ttk.Button(root, text="Forgot password", command=forgot_password)
button_forgot_pass.place(x=60, y=200)
designed = ttk.Label(root, text="Developed by William Cezar")
designed.place(x=30, y=280)

root.mainloop()


