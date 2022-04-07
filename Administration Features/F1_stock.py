# ===================================================TKINTER IMPORTS====================================================
from tkinter import *
from tkinter import ttk
# =====================================================OTHER IMPORTS====================================================
import sys
import os
import subprocess
import tempfile
# =====================================================DATABASE IMPORT==================================================
import sqlite3
import Feature_01.F1_database


# ===================================================MAIN CLASS=========================================================
class Stock:
    def __init__(self, master):
        self.master = master

        # Variables for Functions
        self.product_id = StringVar()
        self.product_name = StringVar()
        self.category_id = StringVar()
        self.quantity = StringVar()
        self.price = StringVar()

        # Implementing Function for Print Button
        def print_data():
            # Making a global variable
            global opener

            # Function to create a text file
            q = self.stock_list.get("1.0", "end-1c")
            filename = tempfile.mktemp("stock_check.txt")

            # Making connection with the database
            con = sqlite3.connect("./AAT_Data.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM product")  # SQL query
            rows = cur.fetchall()  # Getting all the data in a row from the database
            con.close()  # Closing the database

            # Opening File and Writing Function
            f = open(filename, "w")
            f.write(q)
            for row in rows:
                f.write(str(row))
            f.close()

            # Implementing a windows platform for mac, this wouldn't be required for windows
            if sys.platform == "win32":
                os.startfile(filename, "print")
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, filename])

        # Implementing Function for Display Button
        def display_data():
            result = Feature_01.F1_database.stock_check()  # Getting the data from the database
            self.product_list.delete(*self.product_list.get_children())  # Clears the entries
            for row in result:
                # Inserts the data from database to treeview
                self.product_list.insert('', END, values=(row[0], row[1], row[3]))

        # ===============================================FRAMES=========================================================
        # Main Frame
        main_frame = Frame(self.master, bd=10, width=1350, height=700, relief=RIDGE, bg="cadet blue")
        main_frame.grid()

        # Top Frame
        top_frame1 = Frame(main_frame, bd=5, width=1340, height=50, relief=RIDGE)
        top_frame1.grid(row=2, column=0, pady=8)
        tittle_frame = Frame(main_frame, bd=7, width=1340, height=100, relief=RIDGE)
        tittle_frame.grid(row=0, column=0)
        top_frame3 = Frame(main_frame, bd=5, width=1340, height=500, relief=RIDGE)
        top_frame3.grid(row=1, column=0, sticky=W)

        # Right Frame
        right_frame1 = Frame(top_frame3, bd=5, width=600, height=100, padx=2, bg="cadet blue", relief=RIDGE)
        right_frame1.pack()
        right_frame1a = Frame(right_frame1, bd=5, width=600, height=100, padx=2, pady=4, relief=RIDGE)
        right_frame1a.pack(side=TOP, padx=0, pady=4)

        # Tittle Frame
        self.tittle_label = Label(tittle_frame, font=('arial', 40, 'bold'), text="Stock Management",
                                  bd=7)
        self.tittle_label.grid(row=0, column=0, padx=70)

        # =============================================TREEVIEW=========================================================
        # Scroll Bar Function
        scroll_y = Scrollbar(right_frame1a, orient=VERTICAL)  # Setting position of the scroll bar

        self.product_list = ttk.Treeview(right_frame1a, height=18,
                                         column=("Product ID", "Product Name", "Quantity"),
                                         yscrollcommand=scroll_y.set)

        scroll_y.pack(side=RIGHT, fill=Y)  # Configuring the scroll bar

        # Treeview Heading
        self.product_list.heading("Product ID", text="Product ID")
        self.product_list.heading("Product Name", text="Product Name")
        self.product_list.heading("Quantity", text="Quantity")

        self.product_list['show'] = 'headings'

        # Treeview Column
        self.product_list.column("Product ID", width=250, anchor=CENTER)
        self.product_list.column("Product Name", width=260, anchor=CENTER)
        self.product_list.column("Quantity", width=250, anchor=CENTER)

        # Treeview Re-Size
        self.product_list.pack(fill=BOTH, expand=1)
        self.product_list.bind("<ButtonRelease-1>")

        # Treeview Bottom Heading
        self.stock_list = Text(right_frame1a, width=80, height=1, font=('arial', 5, 'bold'))
        self.stock_list.pack()

        self.stock_list.insert(END, "Product ID\t\t\t\t Product Name\t\t\t\t Quantity\t\t\n")

        # =================================================BUTTONS======================================================
        # Button For Display Data
        self.display_bt = Button(top_frame1, pady=1, bd=4, font=('arial', 20, 'bold'), text="Display", width=11,
                                 height=2, command=display_data).grid(row=0, column=0, padx=1)

        # Button For Print Data
        self.display_bt = Button(top_frame1, pady=1, bd=4, font=('arial', 20, 'bold'), text="Print", width=11,
                                 height=2, command=print_data).grid(row=0, column=2, padx=1)


if __name__ == '__main__':
    root = Tk()
    root.geometry("467x488")  # Size of the page
    application = Stock(root)
    root.mainloop()
