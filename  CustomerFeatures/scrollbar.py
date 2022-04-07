from tkinter import *
import tkinter as ttk


class XScrollbar(ttk.Frame):
    # class specifically for implementing scrollbar
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        canvas = Canvas(self, width=880, height=380)
        scrollbar = Scrollbar(self, orient=HORIZONTAL, command=canvas.xview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(xscrollcommand=scrollbar.set)

        canvas.pack(fill="both", expand=True)
        scrollbar.pack(side=BOTTOM, fill=X)


class YScrollbar(ttk.Frame):
    # class specifically for implementing scrollbar
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)
        canvas = Canvas(self, width=860, height=380)
        scrollbar = Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        self.scrollable_f = ttk.Frame(canvas)

        self.scrollable_f.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_f, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=0, column=0)
        scrollbar.grid(row=0, column=1, sticky=NS)
