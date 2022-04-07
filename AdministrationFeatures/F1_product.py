# ===================================================TKINTER IMPORTS====================================================
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
# =====================================================DATABASE IMPORT==================================================
import Feature_01.F1_database
import sqlite3
# =====================================================OTHER IMPORTS====================================================
import subprocess
import sys
import tempfile
import os


# ===================================================MAIN CLASS=========================================================
class Product:
    def __init__(self, master):
        self.master = master

        # Variables for Functions
        self.product_id = StringVar()
        self.product_name = StringVar()
        self.category_id = StringVar()
        self.quantity = StringVar()
        self.price = StringVar()

        # ==============================================FUNCTIONS=======================================================
        # Implementing Function to Clear the Entries
        def clear():
            self.pd_entry.delete(0, END)
            self.name_entry.delete(0, END)
            self.ctg_entry.delete(0, END)
            self.quantity_entry.delete(0, END)
            self.price_entry.delete(0, END)

        # Implementing Function for Add Button
        def add_data():
            try:
                if self.product_id.get() == "" or self.product_name.get() == "" or self.category_id.get() == "" \
                        or self.quantity.get() == "" or self.price.get() == "":
                    messagebox.showinfo("Warning!", "Enter All Field")  # Warning Message Pop
                else:
                    Feature_01.F1_database.add_product(self.product_id.get(), self.product_name.get(),
                                                       self.category_id.get(),
                                                       self.quantity.get(), self.price.get())
            except sqlite3.IntegrityError:
                messagebox.showerror("Warning!", "Product Already Exist!")  # Warning Message Pop
            clear()

        # Implementing Function for Display Button
        def display_data():
            result = Feature_01.F1_database.view_product()  # Getting the data from the database
            self.product_list.delete(*self.product_list.get_children())  # Clears the entries
            for row in result:
                self.product_list.insert('', END, values=row)  # Inserts the data from database to treeview

        # Implementing Function for Delete Button
        def delete_data():
            pd_id = self.product_id.get()  # Setting up variable names
            con = sqlite3.connect("./AAT_Data.db")  # Making connection with the database
            cur = con.cursor()

            # Warning Message Pop
            if messagebox.askyesno("Confirm Delete!", "Are You Sure You Want To Delete This Category?"):

                # SQL query
                cur.execute("DELETE FROM product WHERE id= " + pd_id)
                clear()  # Clears the the entries
                con.commit()  # Used to refresh when making changes
                con.close()  # Closing the database
            else:
                return True

        # Implementing Function for Update Button
        def update_data():
            # Setting up variable names
            edit_id = self.product_id.get()
            edit_name = self.product_name.get()
            edit_category = self.category_id.get()
            edit_quantity = self.quantity.get()
            edit_price = self.price.get()

            # Making connection with the database
            con = sqlite3.connect("./AAT_Data.db")
            cur = con.cursor()

            # Warning Message Pop
            if messagebox.askyesno("Confirm Please!", "Are You Sure You Want to Update This Category?"):

                # SQL query
                cur.execute("UPDATE product SET product_name=?, category_id=?, quantity=?, price=? WHERE id=?",
                            (edit_name, edit_category, edit_quantity, edit_price, edit_id,))
                clear()  # Clears the the entries
                con.commit()  # Used to refresh when making changes
                con.close()  # Closing the database
            else:
                return True

        # Implementing Function for Adding Data on the Treeview
        def product_rec(event):
            # Function to be able to select data from the treeview
            item = self.product_list.item(self.product_list.focus())

            # Setting the values for the inputted data to be displayed in the treeview
            self.product_id.set(item['values'][0])
            self.product_name.set(item['values'][1])
            self.category_id.set(item['values'][2])
            self.quantity.set(item['values'][3])
            self.price.set(item['values'][4])

        # Implementing Function for Print Button
        def print_data():
            # Making a global variable
            global opener

            # Function to create a text file
            q = self.product_check.get("1.0", "end-1c")
            filename = tempfile.mktemp("product_list.txt")

            # Making connection with the database & query
            con = sqlite3.connect("./AAT_Data.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM product")
            rows = cur.fetchall()  # Getting all the data in a row from the database
            con.close()

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

        # Left Frame
        left_frame = Frame(top_frame3, bd=5, width=1340, height=400, padx=2, bg="cadet blue", relief=RIDGE)
        left_frame.pack(side=LEFT)
        left_frame1 = Frame(left_frame, bd=5, width=600, height=100, padx=2, pady=4, relief=RIDGE)
        left_frame1.pack(side=TOP, padx=0, pady=4)

        # Right Frame
        right_frame1 = Frame(top_frame3, bd=5, width=320, height=400, padx=2, bg="cadet blue", relief=RIDGE)
        right_frame1.pack(side=RIGHT)
        right_frame1a = Frame(right_frame1, bd=5, width=310, height=200, padx=2, pady=2, relief=RIDGE)
        right_frame1a.pack(side=TOP)

        # Tittle Frame
        self.tittle_label = Label(tittle_frame, font=('arial', 36, 'bold'), text="Product Management",
                                  bd=7)
        self.tittle_label.grid(row=0, column=0, padx=70)

        # Widget
        self.pd_label = Label(left_frame1, font=('arial', 12, 'bold'), text="Product ID: ", bd=7, anchor=W,
                              justify=LEFT)
        self.pd_label.grid(row=0, column=0, sticky=W, padx=5)
        self.pd_entry = Entry(left_frame1, font=('arial', 12, 'bold'), bd=7, width=30, justify=LEFT,
                              textvariable=self.product_id)
        self.pd_entry.grid(row=0, column=1)

        self.name_label = Label(left_frame1, font=('arial', 12, 'bold'), text="Product Name: ", bd=7, anchor=W,
                                justify=LEFT)
        self.name_label.grid(row=1, column=0, sticky=W, padx=5)
        self.name_entry = Entry(left_frame1, font=('arial', 12, 'bold'), bd=7, width=30, justify=LEFT,
                                textvariable=self.product_name)
        self.name_entry.grid(row=1, column=1)

        self.ctg_label = Label(left_frame1, font=('arial', 12, 'bold'), text="Category ID: ", bd=7, anchor=W,
                               justify=LEFT)
        self.ctg_label.grid(row=2, column=0, sticky=W, padx=5)
        self.ctg_entry = Entry(left_frame1, font=('arial', 12, 'bold'), bd=7, width=30, justify=LEFT,
                               textvariable=self.category_id)
        self.ctg_entry.grid(row=2, column=1)

        self.quantity_label = Label(left_frame1, font=('arial', 12, 'bold'), text="Quantity: ", bd=7, anchor=W,
                                    justify=LEFT)
        self.quantity_label.grid(row=3, column=0, sticky=W, padx=5)
        self.quantity_entry = Entry(left_frame1, font=('arial', 12, 'bold'), bd=7, width=30, justify=LEFT,
                                    textvariable=self.quantity)
        self.quantity_entry.grid(row=3, column=1)

        self.price_label = Label(left_frame1, font=('arial', 12, 'bold'), text="Price: ", bd=7, anchor=W,
                                 justify=LEFT)
        self.price_label.grid(row=4, column=0, sticky=W, padx=5)
        self.price_entry = Entry(left_frame1, font=('arial', 12, 'bold'), bd=7, width=30, justify=LEFT,
                                 textvariable=self.price)
        self.price_entry.grid(row=4, column=1)

        # =============================================TREEVIEW=========================================================
        # Scroll Bar Function
        scroll_y = Scrollbar(right_frame1a, orient=VERTICAL)  # Setting position of the scroll bar

        self.product_list = ttk.Treeview(right_frame1a, height=19,
                                         column=("Product ID", "Product Name", "Category ID", "Quantity", "Price"),
                                         yscrollcommand=scroll_y.set)

        scroll_y.pack(side=RIGHT, fill=Y)  # Configuring the scroll bar

        # Treeview Heading
        self.product_list.heading("Product ID", text="Product ID")
        self.product_list.heading("Product Name", text="Product Name")
        self.product_list.heading("Category ID", text="Category ID")
        self.product_list.heading("Quantity", text="Quantity")
        self.product_list.heading("Price", text="Price")

        self.product_list['show'] = 'headings'

        # Treeview Column
        self.product_list.column("Product ID", width=70, anchor=CENTER)
        self.product_list.column("Product Name", width=100, anchor=CENTER)
        self.product_list.column("Category ID", width=70, anchor=CENTER)
        self.product_list.column("Quantity", width=71, anchor=CENTER)
        self.product_list.column("Price", width=70, anchor=CENTER)

        # Treeview Re-Size
        self.product_list.pack(fill=BOTH, expand=1)
        self.product_list.bind("<ButtonRelease-1>", product_rec)

        # Treeview Bottom Heading
        self.product_check = Text(right_frame1a, width=80, height=1, font=('arial', 5, 'bold'))
        self.product_check.pack()

        self.product_check.insert(END, "Product ID\t\t Product Name\t\t Category ID\t\t Quantity\t\t Price\t\n")

        # =================================================BUTTONS======================================================
        # Button For Add Data
        self.add_bt = Button(top_frame1, pady=1, bd=4, font=('arial', 20, 'bold'), text="Add", width=10, height=2,
                             command=add_data).grid(row=0, column=0, padx=1)

        # Button For Display Data
        self.display_bt = Button(top_frame1, pady=1, bd=4, font=('arial', 20, 'bold'), text="Display", width=11,
                                 height=2, command=display_data).grid(row=0, column=1, padx=1)

        # Button For Delete Data
        self.delete_bt = Button(top_frame1, pady=1, bd=4, font=('arial', 20, 'bold'), text="Delete", width=11,
                                height=2, command=delete_data).grid(row=0, column=2, padx=1)

        # Button For Update Data
        self.update_bt = Button(top_frame1, pady=1, bd=4, font=('arial', 20, 'bold'), text="Update", width=10,
                                height=2, command=update_data).grid(row=0, column=3, padx=1)

        # Button For Print Data
        self.save_bt = Button(top_frame1, pady=1, bd=4, font=('arial', 20, 'bold'), text="Print", width=10,
                              height=2, command=print_data).grid(row=0, column=4, padx=1)


if __name__ == '__main__':
    root = Tk()
    root.title("Product Database Management System")  # Tittle name
    root.geometry("836x433")  # Size of the page
    application = Product(root)
    root.mainloop()
