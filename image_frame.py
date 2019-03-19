from tkinter import *
from PIL import ImageTk, Image
import os


class ImageFrame:
    def __init__(self, master, anchor, init_img_file, frame_dim=300):
        if os.path.isfile(init_img_file) is False:
            raise FileNotFoundError('Default image path does not match')
        self.img = ImageTk.PhotoImage(file=init_img_file)
        self.img_label = None
        self.master = master
        self.frame_dim = frame_dim
        # generate canvas to hold images
        self.canvas = Canvas(self.master,
                             relief='solid',
                             bd=2,
                             width=frame_dim,
                             height=frame_dim)
        self.canvas.place(relx=0.5, rely=0.47, anchor=anchor)
        # configure placeholder image
        self.img_label = Label(self.canvas, image=self.img)
        self.img_label.configure(image=self.img)
        self.img_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        # configure animation variables
        self.is_loading = False
        self.anim_generator = None

    def update_img(self, img_file):
        self.is_loading = False
        self.img = img_file
        self.img_label.configure(image=img_file)

    def init_animation(self, anim):
        self.anim_generator = anim
        self.master.after_idle(self.anim_generator)

    def loading_anim(self):
        self.is_loading = True
        angle = 0
        loading_img = Image.open(os.path.join(os.getcwd(), 'loading_img.png'))
        while True:
            try:
                if self.is_loading:
                    self.master.after_idle(self.anim_generator)
                    self.img = ImageTk.PhotoImage(loading_img.rotate(angle))
                    self.img_label.configure(image=self.img)
                yield
                angle -= 1
                angle %= 360
            except StopIteration as e:
                break



