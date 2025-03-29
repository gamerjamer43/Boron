from .getmasterwidget import get_master_widget
import tkinter as tk

class ScrollBar:
    """
    A wrapper for tk.Scrollbar.
    
    Usage (Boron):
        sb = ScrollBar(parent, orient="vertical")
        sb.pack(side="right", fill="y")
    """
    def __init__(self, master, orient="vertical", **kwargs):
        master_widget = get_master_widget(master)
        self.scrollbar = tk.Scrollbar(master_widget, orient=orient, **kwargs)

    def pack(self, **kwargs):
        self.scrollbar.pack(**kwargs)

    def set(self, lo, hi):
        self.scrollbar.set(lo, hi)

    def config(self, **kwargs):
        self.scrollbar.config(**kwargs)
