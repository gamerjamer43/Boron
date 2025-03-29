from .getmasterwidget import get_master_widget
import tkinter as tk

class Slider:
    """
    A wrapper for tkinter.Scale (slider).
    
    Usage (Boron):
        Slider slider = new Slider(parent, from_=0, to=100, orient="horizontal")
        slider.pack()
        int value = slider.get()
    """
    def __init__(self, master, from_=0, to=100, orient="horizontal", **kwargs):
        master_widget = get_master_widget(master)
        self.scale = tk.Scale(master_widget, from_=from_, to=to, orient=orient, **kwargs)

    def pack(self, **kwargs):
        self.scale.pack(**kwargs)

    def get(self):
        return self.scale.get()

    def set(self, value):
        self.scale.set(value)