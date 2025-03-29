from .getmasterwidget import get_master_widget
import tkinter as tk

class ListBox:
    """
    A wrapper for tkinter.Listbox.
    
    Usage:
        ListBox lb = new ListBox(parent)
        lb.pack()
        lb.insert("end", "Item 1")
        str selected = lb.get_selected()
        list all_items = lb.get_all()
    """
    def __init__(self, master, **kwargs):
        master_widget = get_master_widget(master)
        self.listbox = tk.Listbox(master_widget, **kwargs)

    def pack(self, **kwargs):
        self.listbox.pack(**kwargs)

    def insert(self, index, item):
        self.listbox.insert(index, item)

    def delete(self, index):
        self.listbox.delete(index)

    def get_selected(self):
        selected = self.listbox.curselection()
        if selected:
            return self.listbox.get(selected[0])
        return None

    def get_all(self):
        return list(self.listbox.get(0, tk.END))