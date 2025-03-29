from .getmasterwidget import get_master_widget
import tkinter as tk

class CheckBox:
    """
    A wrapper for tkinter.Checkbutton.
    
    Usage (Boron):
        CheckBox cb = new CheckBox(parent, text="Accept", variable=my_var)
        cb.pack()
    """
    def __init__(self, master, text="", variable=None, **kwargs):
        master_widget = get_master_widget(master)
        self.variable = variable if variable else tk.BooleanVar()
        self.checkbox = tk.Checkbutton(master_widget, text=text, variable=self.variable, **kwargs)

    def pack(self, **kwargs):
        self.checkbox.pack(**kwargs)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)