from tkinter import *
from PIL import Image, ImageTk
import os

default_x_pos = 0.94


class ClrIntensityToggle:
    def __init__(self, master, page_mgr):
        self.master = master
        self.page_mgr = page_mgr
        btn_path_inte_up = os.path.join(os.getcwd(),
                                            'images',
                                            'icons',
                                            'brightness_arr.png')
        btn_path_inte_dwn = os.path.join(os.getcwd(),
                                             'images',
                                             'icons',
                                             'brightness_down_arr.png')
        self.inte_up_btn, self.inte_up_img = self.create_toggle_btn(btn_path_inte_up,
                                                                    True)
        self.inte_dwn_btn, self.inte_dwn_img = self.create_toggle_btn(btn_path_inte_dwn)
        self.hide_buttons()

    def hide_buttons(self):
        self.inte_up_btn.place(relx=0.9, rely=10, anchor=N)
        self.inte_dwn_btn.place(relx=0.9, rely=10, anchor=N)

    def create_toggle_btn(self, icon_path, incrementing=False):
        toggle_icon = Image.open(icon_path)
        toggle_icon = ImageTk.PhotoImage(toggle_icon)
        callback = lambda : self.page_mgr.update_brightness(incrementing)
        toggle_btn = Button(self.master,
                            image=toggle_icon,
                            command=callback)
        return toggle_btn, toggle_icon

    def show_btns(self):
        self.inte_dwn_btn.place(relx=default_x_pos, rely=0.53, anchor=N)
        self.inte_up_btn.place(relx=default_x_pos, rely=0.33, anchor=N)
