from .getmasterwidget import get_master_widget
import tkinter as tk

class RadioButton:
    """
    A wrapper for tkinter.Radiobutton.
    
    Usage:
        RadioButton rb = new RadioButton(parent, text="Option 1", variable=var, value=1)
        rb.pack()
    """
    def __init__(self, master, text="", variable=None, value=None, **kwargs):
        master_widget = get_master_widget(master)
        if variable is None:
            variable = tk.StringVar()
        self.variable = variable
        self.radiobutton = tk.Radiobutton(master_widget, text=text, variable=self.variable, value=value, **kwargs)

    def pack(self, **kwargs):
        self.radiobutton.pack(**kwargs)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)