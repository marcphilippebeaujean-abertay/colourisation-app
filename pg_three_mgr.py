from tkinter import *
from image_frame import ImageFrame
from pg_one_mgr import PageManager
from img_processing import create_image_stack, cv2_to_tk_img
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
        self.stats = {
            'MSE': 0,
            'Mean': 0,
            'Max': 0,
            'Min': 0,
            'Std. Dev.': 0
            }
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
        self.show_stats_btn = Checkbutton(
            self, text="Show Stats", variable=self.show_stats,
        )
        self.show_stats_btn.place(relx=1.12,
                               rely=0.3,
                               anchor=N)

    def on_new_model_selected(self, *kwargs):
        self.queue.put((None,
                        self.tk_model_dir.get()))
        self.output_img.init_animation(self.output_img.loading_anim().__next__)

    def on_prediction_received(self, pred_data):
        # 0 = output_images, 1 = predicted chrominance, 2 = mse
        img_data = pred_data[0]
        if self.should_shuffle.get():
            np.random.shuffle(img_data)
        image_stack = create_image_stack(img_data)
        image_stack = cv2_to_tk_img(image_stack)
        self.output_img.update_img(image_stack)
        self.stats['MSE'] = pred_data[2]

