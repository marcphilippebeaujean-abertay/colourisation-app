from tkinter import *
from wind import Window
from colourisation_manager import ColourisationManager

# Define window
root = Tk()
root.resizable(False, False)
root.geometry('800x350')
# Initialise ui definitions class
wind = Window(root)
clr_mgr = ColourisationManager(root)
# Run application
root.mainloop()