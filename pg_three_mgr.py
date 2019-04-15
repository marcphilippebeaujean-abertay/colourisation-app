from tkinter import *
from image_frame import ImageFrame
from pg_one_mgr import PageManager
from img_processing import create_image_stack, cv2_to_tk_img
from PIL import ImageTk
import os
import numpy as np


class SetPredictionManager(PageManager):
    def __init__(self, master, client, queue, pred_mode='set_pred', width=900, height=400):
        PageManager.__init__(self, master, client, pred_mode, width=width, height=height)
        self.configure(padx=300)
        # define default widget images
        self.output_img = ImageFrame(self,
                                     CENTER,
                                     os.path.join(os.getcwd(),
                                                  'images',
                                                  'icons',
                                                  'blank.png'))
        self.tk_model_dir = StringVar(master)
        choices = {'c_ae_model', 'dil_ae_model', 'lat_ae_model', 'cont_ae_model'}
        self.tk_model_dir.set('c_ae_model')
        self.tk_model_dir.trace('w', self.on_new_model_selected)
        self.model_toggle = OptionMenu(self.output_img.canvas, self.tk_model_dir, *choices)
        self.model_toggle.place(relx=0.5,
                                rely=0.8915,
                                anchor=N)
        self.queue = queue
        self.stats = None
        self.should_shuffle = BooleanVar()
        self.should_shuffle.set(False)
        self.shuffle_btn = Checkbutton(
            self, text="Shuffle", variable=self.should_shuffle,
        )
        self.shuffle_btn.place(relx=1.12,
                               rely=0,
                               anchor=N)
        self.show_stats = BooleanVar()
        self.show_stats.set(False)
        self.show_stats.trace('w', self.switch_display)
        self.show_stats_btn = Checkbutton(
            self, text="Show Stats", variable=self.show_stats,
        )
        self.show_stats_btn.place(relx=1.1644,
                                  rely=0.1,
                                  anchor=N)
        self.image_stack = None
        self.stats_txt = []
        self.pred_pending = False

    def on_new_model_selected(self, *kwargs):
        blank_img = ImageTk.PhotoImage(file=os.path.join(os.getcwd(),
                                                         'images',
                                                         'icons',
                                                         'blank.png'))
        self.output_img.update_img(blank_img)
        if self.pred_pending:
            return
        self.pred_pending = True
        self.forget_stats()
        self.queue.put((None,
                        self.tk_model_dir.get()))
        self.output_img.init_animation(self.output_img.loading_anim().__next__)

    def on_prediction_received(self, pred_data):
        # 0 = output_images, 1 = predicted chrominance, 2 = mse
        self.pred_pending = False
        img_data = pred_data[0]
        if self.should_shuffle.get():
            np.random.shuffle(img_data)
        self.image_stack = create_image_stack(img_data)
        self.image_stack = cv2_to_tk_img(self.image_stack)
        self.update_stats(pred_data[2], pred_data[1])
        self.switch_display()

    def switch_display(self, *kwargs):
        if self.pred_pending:
            return
        if self.stats is None:
            return
        self.forget_stats()
        if self.show_stats.get() is True:
            blank_img = ImageTk.PhotoImage(file=os.path.join(os.getcwd(),
                                                             'images',
                                                             'icons',
                                                             'blank.png'))
            self.output_img.update_img(blank_img)
            self.display_stats()
        else:
            if self.image_stack is not None:
                self.output_img.update_img(self.image_stack)

    def update_stats(self, mse, ab_channels):
        self.stats = {
            'Mean': (np.mean(ab_channels[..., :1]),
                     np.mean(ab_channels[..., 1:])),
            'Max': (np.amax(ab_channels[..., :1]),
                    np.amax(ab_channels[..., 1:])),
            'Min': (np.amin(ab_channels[..., :1]),
                    np.amin(ab_channels[..., 1:])),
            'Std. Dev.': (np.std(ab_channels[..., :1]),
                          np.std(ab_channels[..., 1:])),
            'MSE': mse
        }

    def forget_stats(self):
        for txt in self.stats_txt:
            txt.place_forget()
        self.stats_txt.clear()

    def display_stats(self, *kwargs):
        self.stats_txt = []
        header = Text(self, height=1, width=20)
        header.insert('1.0', 'Output Statistics')
        header.place(relx=0.6, rely=0.1, anchor=N)
        header.tag_config(tagName='Header', justify=CENTER)
        self.stats_txt.append(header)

        first_col_x = 0.2
        col_spread = 0.3
        row_spread = 0.12
        row_padding = 0.20

        header_a_ch = Text(self, height=1, width=9)
        header_a_ch.insert('1.0', 'A Channel')
        header_a_ch.place(relx=first_col_x+col_spread, rely=row_padding, anchor=N)
        self.stats_txt.append(header_a_ch)

        header_a_ch = Text(self, height=1, width=9)
        header_a_ch.insert('1.0', 'B Channel')
        header_a_ch.place(relx=first_col_x + col_spread*2, rely=row_padding, anchor=N)
        self.stats_txt.append(header_a_ch)

        for i, key in enumerate(self.stats.keys()):
            row_pos = (row_spread*(i+1))+row_padding

            stat = Text(self, height=1, width=9)
            stat.insert('1.0', f'{key}')
            stat.place(relx=first_col_x,
                       rely=row_pos,
                       anchor=N)
            self.stats_txt.append(stat)

            data = self.stats[key]

            if key == 'MSE':
                self.stats_txt.append(val_a)
                mse_txt = Text(self, height=1, width=8)
                mse_txt.insert('1.0', f'{data}')
                mse_txt.place(relx=first_col_x + col_spread,
                            rely=row_pos,
                            anchor=N)
                self.stats_txt.append(mse_txt)
                break

            val_a = Text(self, height=1, width=8)
            val_a.insert('1.0', f'{data[0]}')
            val_a.place(relx=first_col_x+col_spread,
                        rely=row_pos,
                        anchor=N)
            self.stats_txt.append(val_a)
            val_b = Text(self, height=1, width=8)
            val_b.insert('1.0', f'{data[1]}')
            val_b.place(relx=first_col_x + col_spread*2,
                        rely=row_pos,
                        anchor=N)
            self.stats_txt.append(val_b)
        for txt in self.stats_txt:
            txt.configure(font=('helvetica', 12))
        header.configure(font=('helvetica', 16, 'bold'))