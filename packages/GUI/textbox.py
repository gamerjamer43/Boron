from .getmasterwidget import get_master_widget
import tkinter as tk

class TextBox:
    """
    A wrapper for tkinter.Entry (single-line text input).
    
    Usage (Boron):
        TextBox textbox = new TextBox(parent)
        textbox.pack()
        str current_text = textbox.get()
        textbox.set("New text")
    """
    def __init__(self, master, **kwargs):
        master_widget = get_master_widget(master)
        self.textbox = tk.Entry(master_widget, **kwargs)

    def pack(self, **kwargs):
        self.textbox.pack(**kwargs)

    def get(self):
        return self.textbox.get()

    def set(self, text):
        self.textbox.delete(0, tk.END)
        self.textbox.insert(0, text)