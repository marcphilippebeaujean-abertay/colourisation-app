from tkinter import *


class ModelPicker:
    def __init__(self, master):
        self.master = master
        self.tk_model_dir = StringVar(master)
        choices = {'c_ae_model', 'dil_ae_model', 'lat_ae_model'}
        self.tk_model_dir.set('c_ae_model')

        dropdown = OptionMenu(master, self.tk_model_dir, *choices)
        dropdown.place(relx=0.5,
                       rely=0.8915,
                       anchor=N)
