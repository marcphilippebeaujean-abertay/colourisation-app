from tkinter import *


class ModelToggle:
    def __init__(self, master):
        self.master = master
        self.tk_model_dir = StringVar(master)
        choices = {'c_ae_model', 'dil_ae_model', 'lat_ae_model'}
        self.tk_model_dir.set('c_ae_model')

        dropdown = OptionMenu(master, self.tk_model_dir, *choices)
        dropdown.pack(side=BOTTOM)

    def get_cur_model_dir(self):
        return self.tk_model_dir
