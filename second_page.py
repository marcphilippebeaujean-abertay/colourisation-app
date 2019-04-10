from tkinter import *
from first_page import PageManager
from img_processing import prepare_for_prediction, cv2_to_tk_img
import random
import cv2
import os
import numpy as np


class SecondPageWidgetManager(PageManager):
    def __init__(self, master, client, input_queue, out_queue):
        super().__init__(master, False, client)
        self.master = master
        self.output_canvas = []
        self.output_labels = []
        frame_dim = 100
        self.sample_images = np.load(open('image_arr.npy', 'rb'))
        self.sample_labels = np.load(open('labels.npy', 'rb'))
        for i in range(6):
            canvas = Canvas(self,
                            relief='solid',
                            bd=2,
                            width=frame_dim,
                            height=frame_dim)
            col = i if i < 3 else i-3
            row = 0 if i < 3 else 2
            canvas.place(anchor=N,
                         relx=0.32+0.18*col,
                         rely=0.135+0.22*row)
            label = Label(master=canvas)
            label.place(relx=0.5, rely=0.05, anchor=N)
            self.output_labels.append(label)
        self.toggle_b = Button(self, text="Toggle Page", command=self.secure_page_toggle)
        self.toggle_b.place(relx=0.5,
                            rely=0.5,
                            anchor=N)
        self.init_btn = Button(self, text="New Image Set", command=self.generate_quiz_images)
        self.init_btn.place(relx=0.5,
                            rely=0.0,
                            anchor=N)
        self.input_queue = input_queue
        self.out_queue = out_queue
        self.predictions_pending = 0

    def generate_quiz_images(self):
        if self.predictions_pending > 0:
            return
        self.output_images = []
        img_id = random.randint(0, 100)
        img = self.sample_images[img_id]
        label = self.sample_labels[img_id]
        img_prepped = prepare_for_prediction(img)
        self.predictions_pending = 4
        self.input_queue.put((img, '', label))

    def on_prediction_received(self, prediction, chrom):
        # check if predictions are pending
        if self.predictions_pending > 0:
            resize_img = cv2.resize(self.sample_images[0], (90, 90))
            photo_img = cv2_to_tk_img(resize_img)
            self.output_images.append(photo_img)
            self.predictions_pending -= 1
            if self.predictions_pending is 0:
                self.show_images()

    def show_images(self):
        print('showing prediction images!')

    def secure_page_toggle(self):
        # only switch when predictions are not pending
        if self.predictions_pending == 0:
            self.client.switch_page()


