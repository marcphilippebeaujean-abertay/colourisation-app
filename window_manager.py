from tkinter import *


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        # master widget = tk window
        self.master = master
        self.init_window()

    def init_window(self):
        # define window title
        self.master.title('Colour+')
        # let widget take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        # initialise rest of UI
        self.init_dropdown_menus()

    def init_dropdown_menus(self):
        # create dropdown menu instance
        dropdown_menu = Menu(self.master)
        self.master.config(menu=dropdown_menu)
        # create the file object)
        file = Menu(dropdown_menu)
        # add exit button to dropdown
        file.add_command(label="Exit", command=lambda: exit())
        # added "file" to our menu
        dropdown_menu.add_cascade(label="File", menu=file)





