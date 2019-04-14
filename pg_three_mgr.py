from tkinter import *
from image_frame import ImageFrame
from pg_one_mgr import PageManager
import os


class SetPredictionManager(PageManager):
    def __init__(self, master, client, pred_mode='set_pred', width=600, height=400):
        PageManager.__init__(self, master, client, pred_mode, width=width, height=height)
        # define default widget images
        self.source_img = ImageFrame(self,
                                     CENTER,
                                     os.path.join(os.getcwd(),
                                                  'images',
                                                  'icons',
                                                  'upload_logo.png'))
