from tkinter import *
from image_frame import ImageFrame
from pg_one_mgr import PageManager
import os


class SetPredictionManager(PageManager):
    def __init__(self, master, client, queue, pred_mode='set_pred', width=600, height=400):
        PageManager.__init__(self, master, client, pred_mode, width=width, height=height)
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

    def on_new_model_selected(self, *kwargs):
        self.queue.put((None,
                        self.tk_model_dir.get()))
        self.output_img.init_animation(self.output_img.loading_anim().__next__)

    def on_prediction_received(self, prediction_data):
        print('hello world')
