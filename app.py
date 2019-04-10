from tkinter import *
from window_def import Window
from io_manager import IOManager

# define window
root = Tk()
root.resizable(False, False)
root.geometry('800x400')
window = Window(root)
client = IOManager(root)
# run application
root.mainloop()