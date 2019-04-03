from tkinter import *
from window_def import Window
from threaded_client import ThreadedClient

# define window
root = Tk()
root.resizable(False, False)
root.geometry('800x370')
window = Window(root)
client = ThreadedClient(root)
# run application
root.mainloop()