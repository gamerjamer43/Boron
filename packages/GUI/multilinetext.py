from .getmasterwidget import get_master_widget
import tkinter as tk

class MultiLineText:
    """
    A wrapper for tkinter.Text for multi-line text editing.
    
    Usage (Boron):
        MultiLineText mlt = new MultiLineText(parent, width=40, height=10)
        mlt.pack()
        str content = mlt.get()
    """
    def __init__(self, master, **kwargs):
        master_widget = get_master_widget(master)
        self.text = tk.Text(master_widget, **kwargs)

    def pack(self, **kwargs):
        self.text.pack(**kwargs)

    def get(self):
        return self.text.get("1.0", tk.END)

    def set(self, content):
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", content)