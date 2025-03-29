from .getmasterwidget import get_master_widget
import tkinter as tk

class Button:
    """
    A wrapper for tkinter.Button.
    
    Usage:
        Button btn = new Button(parent, text="Click Me", command=my_callback)
        btn.pack()
    """
    def __init__(self, master, text="", command=None, **kwargs):
        master_widget = get_master_widget(master)
        self.button = tk.Button(master_widget, text=text, command=command, **kwargs)

    def pack(self, **kwargs):
        self.button.pack(**kwargs)

    def set_text(self, text):
        self.button.config(text=text)

    def get_text(self):
        return self.button.cget("text")
