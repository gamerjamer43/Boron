from .frame import Frame

class Panel(Frame):
    """
    A specialized Frame for grouping components.
    Behaves like a Frame but can be extended for custom behavior.
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)