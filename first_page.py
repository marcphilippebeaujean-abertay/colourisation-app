from tkinter import *
from tkinter.filedialog import askopenfilename
from img_processing import load_to_canvas, cv2_to_tk_img
from image_frame import ImageFrame
from output_frame import OutputFrame
from model_picker import ModelPicker
import os


class PageManager(Frame):
    def __init__(self, master, is_active, client):
        Frame.__init__(self, master, width=600, height=300)
        self.is_active = is_active
        self.client = client

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
        # initialise label members
        self.error_msg = Label(self,
                               text='',
                               fg='red',
                               font=('Helvetica', 20))
        self.error_msg.place(anchor=N,
                             relx=0.5,
                             rely=0.9)
        # reference to threading queue
        self.input_queue = queue
        # add button for configuring images
        choose_file = Button(self.source_img.canvas,
                             text='Choose File',
                             command=lambda: self.load_img())
        choose_file.place(relx=0.5,
                          rely=0.83,
                          anchor=N)
        self.model_toggle = ModelPicker(self.source_img.canvas)
        self.toggle_b = Button(self, text="Toggle Page", command=self.client.switch_page)
        self.toggle_b.place(relx=0.5,
                            rely=0.5,
                            anchor=N)

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
                self.error_msg.configure(text='')
                # create animation
                self.output_img.init_animation(self.output_img.loading_anim().__next__)
            except:
                self.error_msg.configure(text='Failed to load Image!')
            return

    def on_prediction_received(self, prediction, chrom):
        self.output_img.on_output_generated(cv2_to_tk_img(prediction),
                                            cv2_to_tk_img(chrom))