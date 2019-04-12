from tkinter import *
from img_processing import cv2_to_tk_img
from PIL import ImageTk, Image
import os
import cv2

image_dims = (50, 50)


class MiniPredDisplay(Frame):
    def __init__(self, master, frame_id, position=(0.5, 0.5), frame_dim=100):
        Frame.__init__(self, master, width=600, height=300)
        self.image = None
        self.frame_id = frame_id
        self.position = position
        self.btn_offset = 0.23
        self.is_ground_truth = False
        self.canvas = Canvas(self.master,
                             relief='solid',
                             bd=2,
                             width=frame_dim,
                             height=frame_dim)
        self.canvas.place(anchor=N, relx=position[0], rely=position[1])
        self.img_label = Label(master=self.canvas)
        self.img_label.place(relx=0.5, rely=0.25, anchor=N)
        self.img_label.configure(image=self.image)
        self.reveal_text = Label(self.master, text='')
        self.reveal_text.place(anchor=N,
                               relx=position[0],
                               rely=position[1]-0.07)
        self.btn = Button(self.master,
                          text='Select',
                          command=self.on_selected)
        self.btn.place_forget()
        self.model_name = ''
        self.is_loading = False
        self.anim_generator = None

    def update_from_pred(self, pred, is_ground_truth=False):
        self.is_loading = False
        self.is_ground_truth = is_ground_truth
        if is_ground_truth:
            pred = cv2.resize(pred, image_dims)
            self.image = cv2_to_tk_img(pred)
            self.model_name = 'Ground Truth'
        else:
            self.image, _ = pred.generate_output((50, 50))
            self.model_name = pred.model_name
        self.btn.place(anchor=N,
                       relx=self.position[0],
                       rely=self.position[1] + self.btn_offset)
        self.img_label.configure(image=self.image)

    def reset_display(self):
        self.canvas.configure(highlightbackground='white')
        self.model_name = ''
        self.btn.place(anchor=N,
                       relx=self.position[0],
                       rely=self.position[1] + 600)
        self.image = None
        self.reveal_text.configure(text='')

    def on_selected(self):
        self.master.on_pic_selected(self.frame_id)

    def highlight_selection(self):
        if self.is_ground_truth:
            self.canvas.configure(highlightbackground='green')
        else:
            self.canvas.configure(highlightbackground='red')

    def on_revealed(self):
        self.reveal_text.configure(text=self.model_name)

    def update_img(self, img_file):
        self.is_loading = False
        self.image = img_file
        if img_file is None:
            self.img_label.configure(image=self.blank_img)
        else:
            self.img_label.configure(image=img_file)

    def init_animation(self, anim):
        self.anim_generator = anim
        self.master.after_idle(self.anim_generator)

    def loading_anim(self):
        self.is_loading = True
        angle = 0
        loading_img = Image.open(os.path.join(os.getcwd(),
                                              'images',
                                              'icons',
                                              'loading_img.png'))
        loading_img = loading_img.resize(image_dims, Image.ANTIALIAS)
        while True:
            try:
                if self.is_loading:
                    self.master.after_idle(self.anim_generator)
                    self.image = ImageTk.PhotoImage(loading_img.rotate(angle))
                    self.img_label.configure(image=self.image)
                yield
                angle -= 1
                angle %= 360
            except StopIteration as e:
                break

