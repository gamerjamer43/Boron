from .getmasterwidget import get_master_widget
from tkinter import ttk

class ComboBox:
    """
    A wrapper for ttk.Combobox.
    
    Usage:
        ComboBox cb = new ComboBox(parent, values=["One", "Two", "Three"])
        cb.pack()
        str current = cb.get()
    """
    def __init__(self, master, values=None, **kwargs):
        master_widget = get_master_widget(master)
        self.combobox = ttk.Combobox(master_widget, values=values, **kwargs)

    def pack(self, **kwargs):
        self.combobox.pack(**kwargs)

    def get(self):
        return self.combobox.get()

    def set(self, value):
        self.combobox.set(value)