def get_master_widget(master):
    """Helper: return the underlying tk widget from a TkApplication or container."""
    if hasattr(master, "root"):
        return master.root
    elif hasattr(master, "frame"):
        return master.frame
    else:
        return master