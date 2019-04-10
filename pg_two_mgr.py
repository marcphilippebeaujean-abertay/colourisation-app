from tkinter import *
from pg_one_mgr import PageManager
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
        test_data_path = os.path.join(os.getcwd(), 'test_data')
        self.sample_images = np.load(open(f'{test_data_path}/image_arr.npy', 'rb'))
        self.sample_labels = np.load(open(f'{test_data_path}/labels.npy', 'rb'))
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
            self.output_canvas.append(canvas)
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
        img_id = random.randint(0, 99)
        print(img_id)
        img = self.sample_images[img_id]
        label = self.sample_labels[img_id]
        img_prepped = prepare_for_prediction(img)
        self.predictions_pending = 4
        self.input_queue.put((img, '', label))

    def on_prediction_received(self, prediction):
        # check if predictions are pending
        if self.predictions_pending > 0:
            resize_img = cv2.resize(prediction, (90, 90))
            photo_img = cv2_to_tk_img(resize_img)
            self.output_images.append(photo_img)
            self.predictions_pending -= 1
            if self.predictions_pending is 0:
                self.show_images()

    def show_images(self):
        print(len(self.output_images))
        for i, img in enumerate(self.output_images):
            self.output_labels[i].configure(image='')
            self.output_labels[i].configure(image=img)



