from tkinter import *
from pg_one_mgr import PageManager
from pred_mini_display import MiniPredDisplay
import random
import os
import numpy as np


class SecondPageWidgetManager(PageManager):
    def __init__(self, master, client, input_queue, out_queue):
        super().__init__(master, False, client)
        self.master = master
        self.output_displays = []
        self.output_preds = []
        frame_dim = 100
        test_data_path = os.path.join(os.getcwd(), 'test_data')
        self.sample_images = np.load(open(f'{test_data_path}/image_arr.npy', 'rb'))
        self.sample_labels = np.load(open(f'{test_data_path}/labels.npy', 'rb'))
        for i in range(6):
            col = i if i < 3 else i-3
            row = 0 if i < 3 else 2
            pred_disp = MiniPredDisplay(self, (0.32+0.18*col, 0.2+0.22*row))
            self.output_displays.append(pred_disp)
        self.init_btn = Button(self, text="New Image Set", command=self.generate_quiz_images)
        self.init_btn.place(relx=0.5, rely=0.0, anchor=N)
        self.input_queue = input_queue
        self.out_queue = out_queue
        self.predictions_pending = 0

    def generate_quiz_images(self):
        if self.predictions_pending > 0:
            return
        self.output_preds = []
        for pred_disp in self.output_displays:
            pred_disp.reset_display()
        img_id = random.randint(0, 99)
        img = self.sample_images[img_id]
        label = self.sample_labels[img_id]
        self.is_pred_pending = True
        self.predictions_pending = 4
        self.input_queue.put((img, '', label))

    def on_prediction_received(self, prediction):
        # check if predictions are pending
        if self.predictions_pending > 0:
            self.output_preds.append(prediction)
            self.predictions_pending -= 1
            if self.predictions_pending is 0:
                self.show_images()
                self.is_pred_pending = False

    def show_images(self):
        random.shuffle(self.output_preds)
        for i, pred in enumerate(self.output_preds):
            self.output_displays[i].update_from_pred(pred)



