import tkinter as tk
from tkinter import ttk

def get_master_widget(master):
    """Helper: return the underlying tk widget from a TkApplication or container."""
    if hasattr(master, "root"):
        return master.root
    elif hasattr(master, "frame"):
        return master.frame
    else:
        return master

class App:
    """
    Main application window.
    
    Usage:
        app = App(title="My App", width=800, height=600)
        app.run()
    """
    def __init__(self, title="BoronTk Application", width=800, height=600):
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}")
        self.components = []  # for tracking added widgets

    def add_component(self, component, **pack_options):
        """
        Add a widget or container to the application.
        The component must implement a pack() method.
        """
        component.pack(**pack_options)
        self.components.append(component)

    def run(self):
        """Run the main application loop."""
        self.root.mainloop()


class Frame:
    """
    A container widget that wraps tkinter.Frame.
    
    Usage:
        frame = Frame(app, bg="lightgray")
        frame.pack(fill="both", expand=True)
    """
    def __init__(self, master, **kwargs):
        master_widget = get_master_widget(master)
        self.frame = tk.Frame(master_widget, **kwargs)

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def add_component(self, component, **pack_options):
        component.pack(**pack_options)


class Panel(Frame):
    """
    A specialized Frame for grouping components.
    Behaves like a Frame but can be extended for custom behavior.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class Button:
    """
    A wrapper for tkinter.Button.
    
    Usage:
        btn = Button(parent, text="Click Me", command=my_callback)
        btn.pack()
    """
    def __init__(self, master, text="", command=None, **kwargs):
        master_widget = get_master_widget(master)
        self.button = tk.Button(master_widget, text=text, command=command, **kwargs)

    def pack(self, **kwargs):
        self.button.pack(**kwargs)

    def set_text(self, text):
        self.button.config(text=text)

    def get_text(self):
        return self.button.cget("text")


class TextBox:
    """
    A wrapper for tkinter.Entry (single-line text input).
    
    Usage:
        textbox = TextBox(parent)
        textbox.pack()
        current_text = textbox.get()
        textbox.set("New text")
    """
    def __init__(self, master, **kwargs):
        master_widget = get_master_widget(master)
        self.textbox = tk.Entry(master_widget, **kwargs)

    def pack(self, **kwargs):
        self.textbox.pack(**kwargs)

    def get(self):
        return self.textbox.get()

    def set(self, text):
        self.textbox.delete(0, tk.END)
        self.textbox.insert(0, text)


class Label:
    """
    A simple wrapper for tkinter.Label.
    
    Usage:
        label = Label(parent, text="Hello World")
        label.pack()
    """
    def __init__(self, master, text="", **kwargs):
        master_widget = get_master_widget(master)
        self.label = tk.Label(master_widget, text=text, **kwargs)

    def pack(self, **kwargs):
        self.label.pack(**kwargs)

    def set_text(self, text):
        self.label.config(text=text)

    def get_text(self):
        return self.label.cget("text")


class CheckBox:
    """
    A wrapper for tkinter.Checkbutton.
    
    Usage:
        cb = CheckBox(parent, text="Accept", variable=my_var)
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


class RadioButton:
    """
    A wrapper for tkinter.Radiobutton.
    
    Usage:
        rb = RadioButton(parent, text="Option 1", variable=var, value=1)
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


class ListBox:
    """
    A wrapper for tkinter.Listbox.
    
    Usage:
        lb = ListBox(parent)
        lb.pack()
        lb.insert("end", "Item 1")
        selected = lb.get_selected()
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
        return self.listbox.get(0, tk.END)


class ComboBox:
    """
    A wrapper for ttk.Combobox.
    
    Usage:
        cb = ComboBox(parent, values=["One", "Two", "Three"])
        cb.pack()
        current = cb.get()
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


class Slider:
    """
    A wrapper for tkinter.Scale (slider).
    
    Usage:
        slider = Slider(parent, from_=0, to=100, orient="horizontal")
        slider.pack()
        value = slider.get()
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


class MultiLineText:
    """
    A wrapper for tkinter.Text for multi-line text editing.
    
    Usage:
        mlt = MultiLineText(parent, width=40, height=10)
        mlt.pack()
        content = mlt.get()
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


class Canvas:
    """
    A wrapper for tkinter.Canvas.
    
    Usage:
        canvas = Canvas(parent, width=300, height=200)
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


class ProgressBar:
    """
    A wrapper for ttk.Progressbar.
    
    Usage:
        pb = ProgressBar(parent, maximum=100)
        pb.pack()
        pb.set(50)
    """
    def __init__(self, master, maximum=100, **kwargs):
        master_widget = get_master_widget(master)
        self.progress = ttk.Progressbar(master_widget, maximum=maximum, **kwargs)

    def pack(self, **kwargs):
        self.progress.pack(**kwargs)

    def set(self, value):
        self.progress['value'] = value

    def get(self):
        return self.progress['value']


class ScrollBar:
    """
    A wrapper for tk.Scrollbar.
    
    Usage:
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
