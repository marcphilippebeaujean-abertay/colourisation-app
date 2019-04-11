from image_frame import ImageFrame
from tkinter import *

dropdown_choices = {'Output', 'Chrominance', 'Stats'}


class OutputFrame(ImageFrame):
    def __init__(self, master, anchor, init_img_file, frame_dim=300):
        super().__init__(master, anchor, init_img_file, frame_dim)
        self.chrominance = None
        self.output = None
        self.dropdown = None
        self.prediction_data = None
        self.tk_display = StringVar(master)
        self.tk_display.set('Output')
        self.tk_display.trace('w', self.on_img_updated)
        self.stats_txt = []

    def on_img_updated(self, *kwargs):
        if self.dropdown is None:
            self.dropdown = OptionMenu(self.canvas, self.tk_display, *dropdown_choices)
            self.dropdown.place(relx=0.5,
                                rely=0.89,
                                anchor=N)
        if self.prediction_data is None:
            return
        if self.tk_display.get() == 'Output':
            self.update_img(self.output)
        if self.tk_display.get() == 'Chrominance':
            self.update_img(self.chrominance)
        if self.tk_display.get() == 'Stats':
            self.update_img(None)
            self.show_stats()

    def on_output_generated(self, prediction_data):
        self.prediction_data = prediction_data
        self.refresh_image_data()

    def refresh_image_data(self):
        self.output, self.chrominance = self.prediction_data.generate_output()
        self.on_img_updated()

    def show_stats(self):
        self.stats_txt = []
        header = Text(self.canvas, height=2, width=30)
        header.pack(CENTER)
        header.insert(END, 'Output Statistics')
        self.stats_txt.append(header)




