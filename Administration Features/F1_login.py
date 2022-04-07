# ===================================================TKINTER IMPORTS====================================================
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as ms
# =====================================================DATABASE IMPORT==================================================
from Feature_01.F1_product import Product
from Feature_01.F1_category import Category
from Feature_01.F1_stock import Stock
import sqlite3


# Making Database (db) and Users (if not exists already) Table at the Start of Program
# Making connection with the database
with sqlite3.connect('./AAT_Data.db') as db:
    cursor = db.cursor()

# SQL query
cursor.execute('CREATE TABLE IF NOT EXISTS user (Username TEXT NOT NULL PRIMARY KEY,Password TEX NOT NULL);')
db.commit()  # Used to refresh when making changes
db.close()  # Closing the database


# ===================================================MAIN CLASS=========================================================
class F1Feature:
    def __init__(self, master):
        # Variable for the Window
        self.master = master
        # Variables for Functions
        self.username = StringVar()
        self.password = StringVar()
        self.new_username = StringVar()
        self.new_password = StringVar()
        # Variable to Create Widgets
        self.widgets()

        self.admin_panel = Frame(self.master)

        # Button(self.admin_panel, text='Back', height=2).place(x=1160, y=100)
        backframe = Frame(self.admin_panel)
        Button(backframe, text='Back', bd=3, font=('', 16), padx=5, pady=5, command=self.log).place(x=1170, y=200)

        nb = ttk.Notebook(self.admin_panel, height=580)

        f1 = Frame(self.admin_panel)
        Product(f1)
        f2 = Frame(self.admin_panel)
        Category(f2)
        f3 = Frame(self.admin_panel)
        Stock(f3)

        nb.add(f1, text='Product Management')
        nb.add(f2, text='Category Management')
        nb.add(f3, text='Stock Management')
        nb.pack()

    # Implementing Function for Login Button
    def login(self):
        # Establishing Connection with the Database (db)
        with sqlite3.connect('./AAT_Data.db') as db:
            cursor = db.cursor()

        # Finding Users Details from Database and Proper Actions Taken
        find_user = 'SELECT * FROM user WHERE Username = ? and Password = ?'
        cursor.execute(find_user, [(self.username.get()), (self.password.get())])
        result = cursor.fetchall()
        if result:
            self.logf.pack_forget()
            self.head['text'] = self.username.get() + '\n Logged In Successfully'
            self.head['pady'] = 100
        elif self.username.get() == 'admin' and self.password.get() == 'python':
            self.logf.pack_forget()
            self.admin_panel.pack()
            self.head.config(text='Admin Panel', font=('', 18, 'bold', 'underline'))
        else:
            ms.showerror('Oops!', "Sorry, we don't seem to recognise your Username or Password. Please try again.")

    # Implementing Function for Register Button
    def new_user(self):
        # Establishing Connection with the Database (db)
        with sqlite3.connect('./AAT_Data.db') as db:
            cursor = db.cursor()

        # Finding Existing Username and Proper Action
        find_user = 'SELECT Username FROM user WHERE Username = ?'
        cursor.execute(find_user, [(self.new_username.get())])
        if cursor.fetchall():
            ms.showerror('Error!', 'Username Taken Try a Different One.')
        else:
            ms.showinfo('Success!', 'Account Created!')
            self.log()
        # Creating New Account for a New User
        insert = 'INSERT INTO user(Username,Password) VALUES(?,?)'
        cursor.execute(insert, [(self.new_username.get()), (self.new_password.get())])
        db.commit()

    # Frames Packing Methods for both Login and Register
    # Frames Packing Methods for Login
    def log(self):
        self.username.set('')
        self.password.set('')
        self.regf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()

    # Frames Packing Methods for Register
    def reg(self):
        self.new_username.set('')
        self.new_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Register Account'
        self.regf.pack()

    # Making Widgets for the Windows Pages
    def widgets(self):
        # Designing Window for Login Page
        self.head = Label(self.master, text='LOGIN', font=('', 35), pady=10)
        self.head.pack()
        self.logf = Frame(self.master, padx=10, pady=10)
        Label(self.logf, text='Username: ', font=('', 20,), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.username, bd=5, font=('', 15)).grid(row=0, column=1)
        Label(self.logf, text='Password: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.password, bd=5, font=('', 15), show='*').grid(row=1, column=1)
        Button(self.logf, text=' Login ', bd=3, font=('', 15), padx=5, pady=5, command=self.login).grid()
        Button(self.logf, text=' Register Account ', bd=3, font=('', 15), padx=5, pady=5,
               command=self.reg).grid(row=2, column=1)
        self.logf.pack()

        # Designing Window for Register Page
        self.regf = Frame(self.master, padx=10, pady=10)
        Label(self.regf, text='Username: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.regf, textvariable=self.new_username, bd=5, font=('', 15)).grid(row=0, column=1)
        Label(self.regf, text='Password: ', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.regf, textvariable=self.new_password, bd=5, font=('', 15), show='*').grid(row=1, column=1)
        Button(self.regf, text='Register', bd=3, font=('', 15), padx=5, pady=5, command=self.new_user).grid()
        Button(self.regf, text='Go to Login', bd=3, font=('', 15), padx=5, pady=5, command=self.log).grid(row=2,
                                                                                                          column=1)


if __name__ == '__main__':
    # Creating Object and Setup Window
    root = Tk()
    root.title('Login Page')
    F1Feature(root)
    root.mainloop()
