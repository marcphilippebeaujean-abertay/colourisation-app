from tkinter import *
from window_manager import Window
from widget_manager import WidgetManager

# Define window
root = Tk()
root.resizable(False, False)
root.geometry('800x350')
# Initialise ui definitions class
window = Window(root)
user_interface = WidgetManager(root)
# Run application
root.mainloop()