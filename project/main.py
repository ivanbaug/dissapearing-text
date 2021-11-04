import tkinter as tk
import tkinter.font as tkFont
from tkinter import Label, ttk, messagebox
from tkinter.constants import CENTER, END, GROOVE, NONE, RIDGE, WORD

import time

FONT_NAME = "Helvetica"


class Window(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.init_parent()

        # Add Style-Theme
        self.style = ttk.Style(self.parent)
        ## Import the tcl file
        self.parent.tk.call("source", "project\\themes\\forest-light.tcl")
        ## Set the theme with the theme_use method
        self.style.theme_use("forest-light")

        # Define fonts
        self.font_practice_box = tkFont.Font(family=FONT_NAME, size=16)
        self.font_title = tkFont.Font(family=FONT_NAME, size=20, weight="bold")
        self.font_info_box = tkFont.Font(family=FONT_NAME, size=12)
        self.font_countdown = tkFont.Font(family=FONT_NAME, size=40, weight="bold")
        # Vars
        self.g = tk.DoubleVar(value=75.0)

        # Title
        self.title_label = ttk.Label(self, text="Write your text", foreground="#008a25")
        self.title_label.grid(
            row=0, column=0, padx=10, pady=5, sticky="nsew", columnspan=2
        )
        self.title_label.configure(font=self.font_title, anchor=CENTER)

        # Create a frame for practice text
        self.entry_frame = ttk.LabelFrame(self, text="Your text", padding=(10, 10))
        self.entry_frame.grid(
            row=2, column=0, padx=10, pady=(10, 10), sticky="nsew", columnspan=2
        )
        # Practice Text
        self.entry = tk.Text(
            self.entry_frame,
            width=50,
            height=8,
            padx=20,
            pady=15,
            wrap=WORD,
            highlightthickness=0,
            borderwidth=0,
        )
        self.entry.configure(font=self.font_practice_box)
        self.entry.config(spacing1=10, spacing2=10)
        # self.practice_text.tag_configure("center", justify="center")

        # self.practice_text.insert("1.0", self.rand_phrase)
        # self.practice_text.tag_add("center", "1.0", "end")
        self.entry.bind("<Key>", self.keystroke)
        self.entry.grid(row=0, column=0)

        self.entry_label = ttk.Label(self, text="Set your timer:")
        self.entry_label.grid(row=3, column=0, padx=10, pady=2, sticky="nsew")
        # self.entry_label.configure(font=self.font_info_box)

        # Spinbox
        spinbox = ttk.Spinbox(self, from_=5, to=120)
        spinbox.insert(0, "5")
        spinbox.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        # Countdown
        self.countdown_frame = ttk.LabelFrame(
            self, text="Countdown", padding=(10, 10), height=100
        )
        self.countdown_frame.grid(
            row=3, column=1, padx=10, pady=(10, 10), sticky="nsew", rowspan=3
        )

        # # Progressbar
        # progress = ttk.Progressbar(
        #     self.countdown_frame, value=0, variable=self.g, mode="determinate"
        # )
        # progress.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Coundown label
        self.cd_label = ttk.Label(self.countdown_frame, text="5", foreground="#4d4c5c")
        self.cd_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.cd_label.configure(font=self.font_countdown)

    def init_parent(self):
        self.parent.title("Write your prompt")
        self.parent.config(padx=20, pady=20)
        self.parent.option_add("*tearOff", False)  # This is always a good idea
        # Make the app responsive
        self.parent.columnconfigure(index=0, weight=1)
        self.parent.columnconfigure(index=1, weight=1)
        self.parent.columnconfigure(index=2, weight=1)
        self.parent.rowconfigure(index=0, weight=1)
        self.parent.rowconfigure(index=1, weight=1)
        self.parent.rowconfigure(index=2, weight=1)

    def keystroke(self, key):
        print(key.char)

    def update_count_data(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    Window(root).pack(fill="both", expand=True)
    root.mainloop()
