from tkinter import *
from first_page import PageManager
from img_processing import prepare_for_prediction
from PIL import ImageTk, Image
import cv2
import os
import numpy as np


class SecondPageWidgetManager(PageManager):
    def __init__(self, master, client, input_queue, out_queue):
        super().__init__(master, False, client)
        self.master = master
        self.output_canvas = []
        self.output_images = []
        network_dirs = os.listdir(os.path.join(os.getcwd(), 'model_info'))
        frame_dim = 100
        self.sample_images = np.load(open('image_arr.npy', 'rb'))
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
            resize_img = cv2.resize(self.sample_images[0], (90, 90))
            photo_img = ImageTk.PhotoImage(image=Image.fromarray(resize_img))
            self.output_images.append(photo_img)
            label = Label(master=canvas, image=self.output_images[len(self.output_images)-1])
            label.place(relx=0.5, rely=0.05, anchor=N)
            label.configure(image=photo_img)
            self.output_canvas.append(label)
        self.toggle_b = Button(self, text="Toggle Page", command=self.client.switch_page)
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

    def generate_quiz_images(self, img_id):
        if self.predictions_pending > 0:
            return
        preds = []
        img = self.sample_images[img_id]
        img_prepped = prepare_for_prediction(img)
        self.predictions_pending = 4

    def periodic_call(self):
        if self.predictions_pending > 0:
            if self.out_queue.empty() is False:
                img = self.out_queue.get()
            self.master.after(200, self.periodic_call)