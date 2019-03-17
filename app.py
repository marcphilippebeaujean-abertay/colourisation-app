from tkinter import *
from threaded_client import ThreadedClient

# define window
root = Tk()
root.resizable(False, False)
root.geometry('800x350')
client = ThreadedClient(root)
# run application
root.mainloop()