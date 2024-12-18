import tkinter as tk
from tkinter import ttk
from tkinter import font
import os
from my_struct import info
from utils import on_quit

class App(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.database_text = tk.StringVar()
        self.gamertag_text = tk.StringVar()
        self.server_info_text = tk.StringVar()
        self.update_job = None

        self.display_label3_font = font.Font(size=10, weight='bold')
        self.home_label_font = font.Font(size=7)

        self.setup_widgets()

    def setup_buttons(self):
        self.button_frame = ttk.LabelFrame(self, text="--TC--", padding=(0, 0), width=50)
        self.button_frame.grid(row=0, column=0, padx=(10, 5), pady=(5, 10), sticky="nws")
        self.button_frame.grid_propagate(False)

        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=0)
        self.button_frame.columnconfigure(2, weight=1)

        self.button1 = ttk.Button(self.button_frame, text="1", width=2, padding=(4, 2), command=self.on_button1_click)
        self.button1.grid(row=0, column=1, padx=0, pady=0)

        self.button2 = ttk.Button(self.button_frame, text="2", width=2, padding=(4, 2), command=self.on_button2_click)
        self.button2.grid(row=1, column=1, padx=5, pady=5)

    def setup_text(self):
        self.home_label = ttk.Label(self.check_frame, text="bilge diff...", font=self.home_label_font)
        self.display_label2 = ttk.Label(self.check_frame, textvariable=self.server_info_text, font=self.display_label3_font)
        self.display_label = ttk.Label(self.check_frame, textvariable=self.gamertag_text)
        self.display_label3 = ttk.Label(self.check_frame, textvariable=self.database_text)
        self.home_label.grid()
        self.display_label3.grid(row=0, column=0, sticky="nsew")
        self.display_label2.grid(row=1, column=0, sticky="nsew")
        self.display_label.grid(row=2, column=0, sticky="nsew")
        self.display_label3.grid_remove()

    def setup_usable_frame(self):
        self.check_frame = ttk.LabelFrame(self, text="Home", padding=(20, 10))
        self.check_frame.grid(row=0, column=1, padx=(5, 10), pady=(5, 10), sticky="nsew")
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def on_button1_click(self):
        self.remove_every_text()
        self.check_frame['text'] = "Player List"
        self.display_label2.grid()
        self.display_label.grid()
        if self.update_job:
            self.after_cancel(self.update_job)
        self.update_display()

    def on_button2_click(self):
        self.remove_every_text()
        self.check_frame['text'] = "Data Base"
        if self.update_job:
            self.after_cancel(self.update_job)
            self.update_job = None
        self.database_text.set("Coming...\nIn next\nUpdateeeeeee")
        self.display_label3.grid()

    def update_display(self):
        str = f"Server Name: {info.server_name}\nStamp ID: {info.stamp_id}\nServer IP: {info.server_ip}"
        self.server_info_text.set(str)
        self.gamertag_text.set('\n'.join(info.gamertags_list))
        self.update_job = self.after(1000, self.update_display)

    def remove_every_text(self):
        self.display_label.grid_remove()
        self.display_label2.grid_remove()
        self.display_label3.grid_remove()
        self.home_label.grid_remove()

    def setup_widgets(self):
        self.setup_buttons()
        self.setup_usable_frame()
        self.setup_text()

def launch_interface():
    root = tk.Tk()
    root.title("")

    theme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Azure-ttk-theme', 'azure.tcl')
    root.tk.call("source", theme_path)
    root.tk.call("set_theme", "dark")

    app = App(root)
    app.grid(row=0, column=0, sticky="nsew")

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    root.update()
    root.minsize(root.winfo_width() + 150, root.winfo_height() + 300)
    x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
    y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
    root.geometry("+{}+{}".format(x_cordinate, y_cordinate))

    root.protocol("WM_DELETE_WINDOW", on_quit)

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    root.mainloop()

if __name__ == '__main__':
    launch_interface()