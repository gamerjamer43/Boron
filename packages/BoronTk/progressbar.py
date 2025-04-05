from .getmasterwidget import get_master_widget
from tkinter import ttk

class ProgressBar:
    """
    A wrapper for ttk.Progressbar.
    
    Usage (Boron):
        ProgressBar pb = new ProgressBar(parent, maximum=100)
        pb.pack()
        pb.set(50)
    """
    def __init__(self, master, maximum=100, **kwargs):
        master_widget = get_master_widget(master)
        self.progress = ttk.Progressbar(master_widget, maximum=maximum, **kwargs)

    def pack(self, **kwargs):
        self.progress.pack(**kwargs)

    def set_value(self, value):
        self.progress['value'] = value

    def get(self):
        return self.progress['value']