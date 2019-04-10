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
        self.dropdown = OptionMenu(self.canvas, self.tk_display, *choices)
        self.dropdown.place(relx=0.5,
                            rely=0.89,
                            anchor=N)
        self.prediction_data = None

    def on_img_updated(self, *kwargs):
        if self.prediction_data is None:
            return
        if self.tk_display.get() == 'Output':
            if self.output is None:
                return
            self.update_img(self.output)
        else:
            if self.chrominance is None:
                return
            self.update_img(self.chrominance)

    def on_output_generated(self, prediction_data):
        self.prediction_data = prediction_data
        self.refresh_image_data()

    def refresh_image_data(self):
        self.output, self.chrominance = self.prediction_data.generate_output()
        self.on_img_updated()

