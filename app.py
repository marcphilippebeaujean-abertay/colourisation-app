from tkinter import *
from window_manager import Window
from widget_manager import WidgetManager

# define window
root = Tk()
root.resizable(False, False)
root.geometry('800x350')
# initialise ui definitions class
window = Window(root)
user_interface = WidgetManager(root)
# run application
root.mainloop()