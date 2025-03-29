from .getmasterwidget import get_master_widget
import tkinter as tk

class Frame:
    """
    A container widget that wraps tkinter.Frame.
    
    Usage:
        Frame frame = new Frame(app, bg="lightgray")
        frame.pack(fill="both", expand=True)
    """
    def __init__(self, master, **kwargs):
        master_widget = get_master_widget(master)
        self.frame = tk.Frame(master_widget, **kwargs)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def add_component(self, component, **pack_options):
        component.pack(**pack_options)