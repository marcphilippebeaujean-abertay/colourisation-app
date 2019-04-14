from tkinter import *
from image_frame import ImageFrame
from pg_one_mgr import PageManager
import os


class SetPredictionManager(PageManager):
    def __init__(self, master, is_active, client, width=600, height=400):
        Frame.__init__(self, master, width=width, height=height)
        # define default widget images
        self.source_img = ImageFrame(self,
                                     E,
                                     None)
