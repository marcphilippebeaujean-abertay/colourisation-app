from tkinter import *
from window_def import Window
from threaded_client import ThreadedClient

# define window
root = Tk()
root.resizable(False, False)
root.geometry('800x350')
window = Window(root)
client = ThreadedClient(root)
root.protocol( "WM_DELETE_WINDOW", lambda : print('window deleted'))
#root.bind("<Destroy>", client.end_application)
# run application
root.mainloop()