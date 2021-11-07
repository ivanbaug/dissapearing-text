import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from tkinter.constants import CENTER, END, WORD

import time
import threading
import json, random

FONT_NAME = "Helvetica"
filepath = "project\\assets\\quotes.json"


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
        self.font_title = tkFont.Font(
            family=FONT_NAME, size=14, weight="bold", slant="italic"
        )
        self.font_info_box = tkFont.Font(family=FONT_NAME, size=12)
        self.font_countdown = tkFont.Font(family=FONT_NAME, size=40, weight="bold")

        # Vars
        self.time_var = 5
        self._start_time = time.perf_counter()
        self._current_time = time.perf_counter() - 3600
        self.count_var = tk.StringVar()
        self.count_var.set(f"{self.time_var}")
        self.is_writing = False
        self.is_counter_running = False
        self.quotes = self.get_quotes()

        temp_quote = random.choice(self.quotes)
        print(temp_quote)
        # Title
        self.title_label = ttk.Label(
            self,
            text=f"{temp_quote['quote']}\n-{temp_quote['author']}",
            foreground="#008a25",
            wraplength=520,
            justify=CENTER,
        )
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
        self.entry.bind("<Key>", self.keystroke)
        self.entry.grid(row=0, column=0)

        # Frame for time customization
        self.info_frame = ttk.LabelFrame(
            self,
            text="Set your countdown (in seconds)",
            padding=(10, 10),
            height=100,
            width=300,
        )
        self.info_frame.grid(
            row=3, column=0, padx=10, pady=(10, 10), sticky="ew", rowspan=3
        )

        # Spinbox
        self.spinbox = ttk.Spinbox(
            self.info_frame,
            from_=5,
            to=120,
            wrap=True,
            width=10,
            textvariable=self.count_var,
        )
        # self.spinbox.insert(0, "5")
        self.spinbox.pack(side="top", padx=10, pady=5)
        self.count_var.trace("w", self.update_count_data)

        # Other information
        self.info_label = ttk.Label(
            self.info_frame,
            text="",
            wraplength=240,
            justify=CENTER,
        )
        self.info_label.pack(side="bottom", padx=10, pady=5)
        # self.info_label.config(anchor=CENTER)

        # Countdown Frame
        self.countdown_frame = ttk.LabelFrame(
            self, text="Countdown", padding=(10, 10), height=100, width=200
        )
        self.countdown_frame.grid(
            row=3, column=1, padx=10, pady=(10, 10), sticky="nsew", rowspan=3
        )
        # Coundown label
        self.cd_label = ttk.Label(
            self.countdown_frame, text=f"{self.time_var}", foreground="#4d4c5c"
        )
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
        self.is_writing = True
        self._start_time = time.perf_counter()
        self.info_label.config(text="")
        if not self.is_counter_running:
            self.is_counter_running = True
            x = threading.Thread(target=self.run_countdown)
            x.start()

    def run_countdown(self):
        while self._start_time + self.time_var > self._current_time:

            self._current_time = time.perf_counter()
            remaining_time = self.time_var - (self._current_time - self._start_time)
            if remaining_time < 0:
                remaining_time = 0
            self.cd_label.config(text=f"{remaining_time:.1f}")
            time.sleep(0.2)
        # once the counter stops
        self.is_counter_running = False
        self.is_writing = False
        self.entry.delete("1.0", END)

    def update_count_data(self, var, indx, mode):
        if self.is_writing:
            self.info_label.config(
                text="The countdown already started, change the timer once it ends."
            )
        else:
            try:
                tvar = self.count_var.get()
                self.time_var = int(tvar)
            except ValueError:
                # Do nothing if gibberish is written on the spinner
                pass
            self.cd_label.config(text=f"{self.time_var}")

    def get_quotes(self):
        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
        return data["quotes"]

    def one_quote(self, quotes):
        return random.choice(quotes)


if __name__ == "__main__":
    root = tk.Tk()
    Window(root).pack(fill="both", expand=True)
    root.mainloop()
