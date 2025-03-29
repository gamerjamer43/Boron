from .getmasterwidget import get_master_widget
import tkinter as tk

class Canvas:
    """
    A wrapper for tkinter.Canvas.
    
    Usage (Boron):
        Canvas canvas = new Canvas(parent, width=300, height=200)
        canvas.pack()
        canvas.create_rectangle(10, 10, 100, 100, fill="blue")
    """
    def __init__(self, master, **kwargs):
        master_widget = get_master_widget(master)
        self.canvas = tk.Canvas(master_widget, **kwargs)

    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)

    def create_rectangle(self, *args, **kwargs):
        return self.canvas.create_rectangle(*args, **kwargs)

    def create_oval(self, *args, **kwargs):
        return self.canvas.create_oval(*args, **kwargs)

    def create_line(self, *args, **kwargs):
        return self.canvas.create_line(*args, **kwargs)

    def create_text(self, *args, **kwargs):
        return self.canvas.create_text(*args, **kwargs)

    def delete(self, item):
        self.canvas.delete(item)