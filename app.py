from tkinter import *
from window_def import Window
from io_manager import IOManager

# define window
root = Tk()
root.resizable(False, False)
root.geometry('800x400')
window = Window(root)
client = IOManager(root)
toggle_b = Button(root, text="Toggle Page", command=client.switch_page)
toggle_b.place(relx=0.5, rely=0.02, anchor=N)
# run application
root.mainloop()