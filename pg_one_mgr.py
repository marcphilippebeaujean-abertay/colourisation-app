from tkinter import *
from tkinter.filedialog import askopenfilename
from img_processing import load_to_canvas, cv2_to_tk_img
from image_frame import ImageFrame
from output_frame import OutputFrame
from model_picker import ModelPicker
import os


class PageManager(Frame):
    def __init__(self, master, is_active, client, width=600, height=400):
        Frame.__init__(self, master, width=width, height=height)
        self.is_active = is_active
        self.client = client
        self.is_pred_pending = False

    def on_page_switch(self):
        self.is_active = not self.is_active

    def on_prediction_received(self, prediction, chrom):
        raise RuntimeError('On prediction undefined')


class ImageUploadPageManager(PageManager):
    def __init__(self, master, queue, client):
        PageManager.__init__(self, master, True, client)
        # define default widget images
        self.source_img = ImageFrame(self,
                                     E,
                                     os.path.join(os.getcwd(),
                                                  'images',
                                                  'icons',
                                                  'upload_logo.png'))
        # generate model output canvas/frame
        self.output_img = OutputFrame(self,
                                      W,
                                      os.path.join(os.getcwd(),
                                                   'images',
                                                   'icons',
                                                   'eye_logo.png'))
        # reference to threading queue
        self.input_queue = queue
        # add button for configuring images
        choose_file = Button(self.source_img.canvas,
                             text='Choose File',
                             command=lambda: self.load_img())
        choose_file.place(relx=0.5,
                          rely=0.82,
                          anchor=N)
        self.model_toggle = ModelPicker(self.source_img.canvas)

    def load_img(self):
        img_path = askopenfilename(initialdir=os.getcwd(),
                                   filetypes=(("PNG File", "*.png"),
                                              ("All Files", "*.*")),
                                   title='Choose an Image')
        if len(img_path) is 0:
            return
        if os.path.isfile(img_path):
            try:
                # adjust image to fit to canvas
                img_source = load_to_canvas(img_path,
                                            (self.source_img.frame_dim-5))
                # add image to the queue
                self.input_queue.put((img_source,
                                      self.model_toggle.tk_model_dir.get()))
                # apply widget updates
                self.source_img.update_img(cv2_to_tk_img(img_source))
                self.client.notification_update('')
                # create animation
                self.output_img.init_animation(self.output_img.loading_anim().__next__)
            except:
                self.client.notification_update('Failed to load Image!', True)
            return

    def on_prediction_received(self, prediction_data):
        self.output_img.on_output_generated(prediction_data)
        self.is_pred_pending = False