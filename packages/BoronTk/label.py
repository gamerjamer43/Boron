from .getmasterwidget import get_master_widget
import tkinter as tk

class Label:
    """
    A simple wrapper for tkinter.Label.
    
    Usage (Boron):
        Label label = new Label(parent, text="Hello World")
        label.pack()
    """
    def __init__(self, master, text="", **kwargs):
        master_widget = get_master_widget(master)
        self.label = tk.Label(master_widget, text=text, **kwargs)

    def pack(self, **kwargs):
        self.label.pack(**kwargs)

    def set_text(self, text):
        self.label.config(text=text)

    def get_text(self):
        return self.label.cget("text")