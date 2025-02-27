from tkinter import Tk, filedialog
from assembler import assemble

# Hide the main Tkinter window
root = Tk()
root.withdraw()

# Open a file dialog to select a .b file
file = filedialog.askopenfilename(
    title="Select a .b file",
    filetypes=[("Boron Files", "*.b")]
)

# Check if a file was selected
if file:
    assemble(file)
else:
    print("No file selected.")
