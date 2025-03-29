import tkinter as tk

class App:
    """
    Main application window.
    
    Usage:
        App app = new App(title="My App", width=800, height=600)
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