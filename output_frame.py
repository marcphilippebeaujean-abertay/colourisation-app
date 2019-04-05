from image_frame import ImageFrame
from tkinter import *


class OutputFrame(ImageFrame):
    def __init__(self, master, anchor, init_img_file, frame_dim=300):
        super().__init__(master, anchor, init_img_file, frame_dim)
        self.chrominance = None
        self.output = None
        choices = {'Output', 'Chrominance'}
        self.tk_display = StringVar(master)
        self.tk_display.trace('w', self.on_img_updated)
        self.tk_display.set('Output')
        self.dropdown = OptionMenu(master, self.tk_display, *choices)
        self.dropdown.place(x=500, y=10)

    def on_img_updated(self, *kwargs):
        if self.tk_display.get() == 'Output':
            if self.output is None:
                return
            self.update_img(self.output)
        else:
            if self.chrominance is None:
                return
            self.update_img(self.chrominance)

    def on_output_generated(self, output_data, chrom):
        self.output = output_data
        self.chrominance = chrom
        self.on_img_updated()

