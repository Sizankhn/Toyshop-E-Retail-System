# ======================== TKINTER IMPORTS ========================================================
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msg
import tkinter.font as font
from tkinter import colorchooser
# =================================================================================================
# ======================== FILE IMPORTS ===========================================================
from CustomerFeatures.scrollbar import XScrollbar, YScrollbar
from CustomerFeatures.F2_database import fetch_name, fetch_price, toyprice, toydescrip, fetch_customer, \
    fetch_rating, fetch_review, fetch_date, check_stock
# =================================================================================================
from datetime import date


class F2Feature:
    def __init__(self, master):
        self.master = master

        # ========================================= FONTS ==============================================================
        fontStyle_4 = font.Font(family="Calibri", weight='bold', size=16)
        txt_font = font.Font(family='Calibri', size='16')
        # ==============================================================================================================
        # ======================================== FUNCTIONS ===========================================================

        def searchitem():  # function for Search bar
            if search.get() in toys_list:
                self.notebook.add(framefortoy, text=search.get())
                self.notebook.select(tab_id=3)
                self.notebook.add(frameFour, text='Write A Review')
                self.notebook.add(frameFive, text='All Reviews')
                toyName.config(text=search.get(), font=('', 16))
                toyPrice.config(text=toyprice(search.get()), font=('', 16))
                toyDescrip.config(text=toydescrip(search.get()), font=('', 16), justify=LEFT)
            else:
                msg.askokcancel('AAToys', 'Sorry, no such toy')

            for customer, rating, review, reviewdate in zip(fetch_customer(search.get()), fetch_rating(search.get()),
                                                            fetch_review(search.get()), fetch_date(search.get())):
                pane = tk.PanedWindow(frameFive.scrollable_f, orient=VERTICAL, bg='black', height=260)
                reviewsframe = LabelFrame(pane, width=500, height=100, text=reviewdate)

                Label(reviewsframe, text='Toy:', font=('', 14, 'bold')).place(x=20, y=30)
                Label(reviewsframe, text=search.get(), font=('', 16)).place(x=60, y=30)

                Label(reviewsframe, text='Customer Name:', font=('', 14, 'bold')).place(x=20, y=70)
                Label(reviewsframe, text=customer, font=('', 16)).place(x=150, y=70)

                Label(reviewsframe, text='Ratings:', font=('', 14, 'bold')).place(x=20, y=110)
                Label(reviewsframe, text=rating, font=('', 16)).place(x=100, y=110)

                Label(reviewsframe, text='Review:', font=('', 14, 'bold')).place(x=20, y=150)
                Message(reviewsframe, text=review, width=400).place(x=90, y=150)
                pane.add(reviewsframe)
                pane.grid(padx=200, pady=10)

        def update(data):
            my_list.delete(0, END)

            for item in data:
                my_list.insert(END, item)

        def fillout(event):
            search.delete(0, END)  # Delete whatever is there in Entry box
            search.insert(0, my_list.get(ACTIVE))  # Delete whatever is there in Entry box

        def check(event):  # function to check Search bar vs Listbox
            typed = search.get()  # grab what was typed
            if typed == '':
                data = toys
            else:
                data = []
                for item in toys:
                    if typed.lower() in item.lower():
                        data.append(item)

            update(data)

        def clear():
            search.delete(0, END)  # Clears whatever is there in Search bar

        def close_tab():
            self.notebook.hide(tab_id=3)  # Hides the ( Toy ) tab
            self.notebook.hide(tab_id=4)  # Hides the ( Write A Review ) tab
            self.notebook.hide(tab_id=5)  # Hides the ( See All Reviews ) tab
            self.notebook.select(tab_id=0)

        def write_review():
            self.notebook.select(tab_id=4)  # Show up ( Write A Review ) tab

        def see_reviews():
            self.notebook.select(tab_id=5)  # Show up ( See All Reviews ) tab

        def bolder():  # function to bold the selected text
            try:
                bold_font = font.Font(text, text.cget("font"))
                bold_font.configure(weight="bold")
                text.tag_configure("bold", font=bold_font)
                current_tags = text.tag_names(SEL_FIRST)
                if "bold" in current_tags:
                    text.tag_remove("bold", SEL_FIRST, SEL_LAST)
                else:
                    text.tag_add("bold", SEL_FIRST, SEL_LAST)
            except TclError:
                msg.showerror('Alert', 'Text needs to be selected')

        def italics():  # function to italicise the selected text
            try:
                italics_font = font.Font(text, text.cget("font"))
                italics_font.configure(slant="italic")
                text.tag_configure("italic", font=italics_font)
                current_tags = text.tag_names(SEL_FIRST)
                if "italic" in current_tags:
                    text.tag_remove("italic", SEL_FIRST, SEL_LAST)
                else:
                    text.tag_add("italic", SEL_FIRST, SEL_LAST)
            except TclError:
                msg.showerror('Alert', 'Text needs to be selected')

        def change_color():  # function to change color of selected text
            try:
                my_color = colorchooser.askcolor()[1]
                if my_color:
                    color_font = font.Font(text, text.cget("font"))
                    text.tag_configure("colored", font=color_font, foreground=my_color)
                    current_tags = text.tag_names(SEL_FIRST)

                    if "colored" in current_tags:
                        text.tag_remove("colored", SEL_FIRST, SEL_LAST)
                    else:
                        text.tag_add("colored", SEL_FIRST, SEL_LAST)
            except TclError:
                msg.showerror('Alert', 'Text needs to be selected')

        def submit():
            """"
            Reviews get stored into database
            """
            if self.customer_name.get() == '' or combo.get() == '' or text.get(1.0, END) == '':
                msg.showerror('ERROR', 'All Field are required')
            else:
                with sqlite3.connect("./python_cw.db") as db:
                    cursor = db.cursor()
                insert = '''
                         INSERT INTO reviews
                         (customer, toy_name, rating, review, review_date) VALUES(?, ?, ?, ?, ?)
                         '''
                data_tuple = (self.customer_name.get(), search.get(), combo.get(), text.get(1.0, END),
                              date.today())
                cursor.execute(insert, data_tuple)
                db.commit()
                cursor.close()
                db.close()
                msg.showinfo('Successful!!', 'Thank you so much!')
                self.customer_name.delete(0, END)
                combo.delete(0, END)
                text.delete(1.0, END)  # to delete the final text

        # ==============================================================================================================
        # ================================ SEARCH BAR & LISTBOX (with toys) ============================================

        self.toyDisplay = PanedWindow(self.master, orient=VERTICAL, height=600, width=300, bg='white')
        self.toyDisplay.grid(row=1, column=0, sticky=NW)

        search = tk.Entry(self.toyDisplay, width=16, font=('', 22), relief=GROOVE)
        search.place(x=20, y=100)

        search.focus()  # automatically get the cursor to the entry_search
        search.bind('<Return>')  # run function when in `entry`, you press `ENTER` on keyboard

        # Search Button
        search_button = tk.Button(self.toyDisplay, text='Search', font=('', 15), width=10, command=searchitem)
        search_button.place(x=30, y=150)

        # Clear Button
        clear_button = tk.Button(self.toyDisplay, text='Clear', width=10, font=('', 15), command=clear)
        clear_button.place(x=150, y=150)

        frame = Frame(self.toyDisplay)  # Create a frame
        my_scrollbar = Scrollbar(frame, orient=VERTICAL)  # Creating a scrollbar

        list_label = Label(frame, text='List of all toys...', fg='grey', font=('', 16))
        list_label.pack(side=TOP)

        my_list = Listbox(frame, width=24, font=('', 16), yscrollcommand=my_scrollbar.set,
                          cursor='top_left_arrow', relief=GROOVE)
        my_scrollbar.config(command=my_list.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y, pady=5)
        frame.place(x=20, y=250)
        my_list.pack(side=BOTTOM, pady=5)

        toys_list = [
            'Monopoly', 'AnimalSoundtrack', 'TalkingRobot', 'Sequence', 'Pop', '5SecondsRule', 'Articulate', 'Dobble',
            'Confident', 'Tension', 'Trekking', 'HotWires', 'Interplay', 'SillySafari', 'ScavengerHunt', 'LEGOCreator',
            'ExplodingKittens', 'FoxyPants', 'MiniAnimals', 'PianoKeyboard', 'MiniDrone', 'LCDTablet', 'Paladone',
            'SnapCircuits'
        ]

        toys = sorted(toys_list)  # List of Toys and Categories

        update(toys)  # Add the toys to our list

        my_list.bind("<<ListboxSelect>>", fillout)  # Create binding on the listbox onclick
        search.bind("<KeyRelease>", check)  # Create binding on the Entry box

        Label(self.toyDisplay, text='Use the arrow keys ⬆️ ⬇️').place(x=55, y=500)

        # ===================================== Notebook with all the toys =============================================

        self.notebook = ttk.Notebook(self.master)

        frameOne = XScrollbar(self.master)  # Board Category
        frameTwo = XScrollbar(self.master)  # Animal Category
        frameThree = XScrollbar(self.master)  # Electronic Category
        framefortoy = Frame(self.master)  # Toy
        frameFour = Frame(self.master)  # Write A Review
        frameFive = YScrollbar(self.master)  # See all reviews

        self.notebook.add(frameOne, text='Board')
        self.notebook.add(frameTwo, text='Animal')
        self.notebook.add(frameThree, text='Electronic')

        board = tk.PanedWindow(frameOne.scrollable_frame, orient=HORIZONTAL, sashpad=1, bg='black', height=380)
        animal = tk.PanedWindow(frameTwo.scrollable_frame, orient=HORIZONTAL, sashpad=1, bg='black', height=380)
        electronic = tk.PanedWindow(frameThree.scrollable_frame, orient=HORIZONTAL, sashpad=1, bg='black', height=380)

        for name, price, st in zip(fetch_name('Board'), fetch_price('Board'), check_stock('Board')):
            self.lblframe1 = tk.LabelFrame(board, padx=10, bd=2)
            t_name = ''.join(name) + '.png'
            img = './assets/board/' + t_name
            self.photo = PhotoImage(file=img)
            self.image = Label(self.lblframe1, image=self.photo, relief=GROOVE, width=200, height=200)
            self.image.photo = self.photo
            self.image.grid(pady=10)
            Label(self.lblframe1, text=name, font=('', 18, 'bold')).grid(pady=2)
            Label(self.lblframe1, text='£', font=txt_font).grid(row=3, column=0, sticky=W, padx=50)
            Label(self.lblframe1, text=price, font=txt_font).grid(row=3, column=0, pady=2)
            Label(self.lblframe1, text='In Stock:', font=('', 16, 'underline')).grid(row=4, column=0, pady=20, sticky=W)
            Label(self.lblframe1, text=st, font=txt_font).grid(row=4, column=0, padx=74, sticky=W)
            board.add(self.lblframe1)
            board.grid()

        for name, price, stock in zip(fetch_name('Animal'), fetch_price('Animal'), check_stock('Animal')):
            self.lblframe2 = tk.LabelFrame(animal, padx=10, bd=2)
            t_name = ''.join(name) + '.png'
            img = './assets/animal/' + t_name
            self.photo = PhotoImage(file=img)
            self.image = Label(self.lblframe2, image=self.photo, relief=GROOVE, width=200, height=200)
            self.image.photo = self.photo
            self.image.grid(pady=10)
            Label(self.lblframe2, text=name, font=('', 18, 'bold')).grid(pady=2)
            Label(self.lblframe2, text='£', font=txt_font).grid(row=3, column=0, sticky=W, padx=50)
            Label(self.lblframe2, text=price, font=txt_font).grid(row=3, column=0, pady=2)
            Label(self.lblframe2, text='In Stock:', font=txt_font).grid(row=4, column=0, pady=20, sticky=W)
            Label(self.lblframe2, text=stock, font=txt_font).grid(row=4, column=0, padx=74, sticky=W)
            animal.add(self.lblframe2)
            animal.grid()

        for name, price, stock in zip(fetch_name('Electronic'), fetch_price('Electronic'), check_stock('Electronic')):
            self.lblframe3 = tk.LabelFrame(electronic, padx=10, bd=2)
            t_name = ''.join(name) + '.png'
            img = './assets/electronic/' + t_name
            self.photo = PhotoImage(file=img)
            self.image = Label(self.lblframe3, image=self.photo, relief=GROOVE, width=200, height=200)
            self.image.photo = self.photo
            self.image.grid(pady=10)
            Label(self.lblframe3, text=name, font=('', 18, 'bold')).grid(pady=2)
            Label(self.lblframe3, text='£', font=txt_font).grid(row=3, column=0, sticky=W, padx=50)
            Label(self.lblframe3, text=price, font=txt_font).grid(row=3, column=0, pady=2)
            Label(self.lblframe3, text='In Stock:', font=txt_font).grid(row=4, column=0, pady=20, sticky=W)
            Label(self.lblframe3, text=stock, font=txt_font).grid(row=4, column=0, padx=74, sticky=W)
            electronic.add(self.lblframe3)
            electronic.grid()
        self.notebook.grid(row=1, column=0, padx=30, pady=80, sticky=E)

        # ==============================================================================================================
        # =========================================TOY-SPECIFIC=========================================================

        name = tk.Label(framefortoy, text='Name:', font=('Helvetica', 16, 'bold'))
        name.place(x=50, y=50)

        toyName = tk.Label(framefortoy, text='')
        toyName.place(x=110, y=50)

        price = tk.Label(framefortoy, text='Price:', font=('Helvetica', 16, 'bold'))
        price.place(x=50, y=100)

        toyPrice = tk.Label(framefortoy, text='')
        toyPrice.place(x=100, y=100)

        # Quantity - Spin Box
        qt_label = tk.Label(framefortoy, text='Quantity:', font=('Helvetica', 16, 'bold'))
        qt_label.place(x=50, y=150)

        toyQuantity = Spinbox(framefortoy, from_=1, to=20, width=7)
        toyQuantity.place(x=130, y=148)

        desc_label = tk.Label(framefortoy, text='Description:', font=('Helvetica', 16, 'bold'))
        desc_label.place(x=350, y=50)

        toyDescrip = Message(framefortoy, text='', width=300)
        toyDescrip.place(x=350, y=75)

        # AddToCart_1
        addtocart_button = tk.Button(framefortoy, text='Add To Cart', width=15, height=2,
                                     fg='Black', bg='white', relief=RIDGE)
        addtocart_button.place(x=60, y=250)

        # Buy Now_1
        buynow_button = tk.Button(framefortoy, text='Buy Now', width=15, height=2,
                                  fg='black', bg='white', relief=RIDGE)
        buynow_button.place(x=60, y=300)

        review_lbl = tk.Label(framefortoy,
                              text='Like the\n'
                                   '  Product?',
                              font=('Helvetica', 22, 'bold'))
        review_lbl.place(x=700, y=160)

        writereview_btn = tk.Button(framefortoy, width=14, text='Write a review', height=2, command=write_review)
        writereview_btn.place(x=700, y=240)

        allreview_btn = tk.Button(framefortoy, width=14, text='See all reviews', height=2, command=see_reviews)
        allreview_btn.place(x=700, y=280)

        close = tk.Button(framefortoy, text='❌', width=6, height=2, command=close_tab)
        close.place(x=800, y=20)

        # ==================================== WRITE A REVIEW ==========================================================

        Label(frameFour, text='* - field input required', fg='red').place(x=730, y=5)

        Label(frameFour, text='Your Name*', font=fontStyle_4).place(x=205, y=20)

        self.customer_name = Entry(frameFour, width=20, relief=GROOVE)
        self.customer_name.place(x=205, y=50)

        Label(frameFour, text='Rating*', font=fontStyle_4).place(x=205, y=90)

        combo = ttk.Combobox(frameFour, width=10, values=("Excellent", "Good", "Fair", "Poor", "Awful"))
        combo.place(x=205, y=120)

        Label(frameFour, text='Review*', font=fontStyle_4).place(x=205, y=165)

        # TextBox Scrollbar
        text_scroll = Scrollbar(frameFour)
        text_scroll.place(x=700, y=200, height=150, anchor=NW)

        text = Text(frameFour, width=30, height=5, font=('', '25'), undo=True, yscrollcommand=text_scroll.set)
        text.place(x=210, y=200, anchor=NW)
        text_scroll.config(command=text.yview)
        text.focus_force()

        # Bold the selected text
        bold = Button(frameFour, text='Bold', width=10, command=bolder)
        bold.place(x=740, y=200)

        # Italic the selected text
        italics = Button(frameFour, text='Italics', width=10, command=italics)
        italics.place(x=740, y=230)

        # Color the selected text
        color = Button(frameFour, text='Change Color', width=10, command=change_color)
        color.place(x=740, y=260)

        # Submit Button
        submit_btn = tk.Button(frameFour, width='10', text='Submit', font=('', 16, 'bold'), command=submit)
        submit_btn.place(x=400, y=360)


if __name__ == '__main__':
    # Creating Object and Setup Window
    root = Tk()
    F2Feature(root)
    root.mainloop()
