from image_frame import ImageFrame
from tkinter import *

dropdown_choices = {'Output', 'Chrominance', 'Stats', 'Activations'}


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
                                rely=0.895,
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
        else:
            for txt in self.stats_txt:
                txt.place_forget()

    def on_output_generated(self, prediction_data):
        self.prediction_data = prediction_data
        self.refresh_image_data()

    def refresh_image_data(self):
        self.output, self.chrominance = self.prediction_data.generate_output()
        self.on_img_updated()

    def show_stats(self):
        self.stats_txt = []
        header = Text(self.canvas, height=1, width=20)
        header.insert('1.0', 'Output Statistics')
        header.place(relx=0.54, rely=0.1, anchor=N)
        header.tag_config(tagName='Header', justify=CENTER)
        self.stats_txt.append(header)

        first_col_x = 0.2
        col_spread = 0.3
        row_spread = 0.12
        row_padding = 0.20

        header_a_ch = Text(self.canvas, height=1, width=9)
        header_a_ch.insert('1.0', 'A Channel')
        header_a_ch.place(relx=first_col_x+col_spread, rely=row_padding, anchor=N)
        self.stats_txt.append(header_a_ch)

        header_a_ch = Text(self.canvas, height=1, width=9)
        header_a_ch.insert('1.0', 'B Channel')
        header_a_ch.place(relx=first_col_x + col_spread*2, rely=row_padding, anchor=N)
        self.stats_txt.append(header_a_ch)

        for i, key in enumerate(self.prediction_data.stats.keys()):
            row_pos = (row_spread*(i+1))+row_padding

            stat = Text(self.canvas, height=1, width=9)
            stat.insert('1.0', f'{key}')
            stat.place(relx=first_col_x,
                       rely=row_pos,
                       anchor=N)
            self.stats_txt.append(stat)

            data = self.prediction_data.stats[key]

            val_a = Text(self.canvas, height=1, width=8)
            val_a.insert('1.0', f'{data[0]}')
            val_a.place(relx=first_col_x+col_spread,
                        rely=row_pos,
                        anchor=N)
            self.stats_txt.append(val_a)
            val_b = Text(self.canvas, height=1, width=8)
            val_b.insert('1.0', f'{data[1]}')
            val_b.place(relx=first_col_x + col_spread*2,
                        rely=row_pos,
                        anchor=N)
            self.stats_txt.append(val_b)




