from tkinter import *
from tkinter.filedialog import askopenfilename
from img_processing import load_to_canvas, cv2_to_tk_img
from prediction_thread import pred_modes
from image_frame import ImageFrame
from output_frame import OutputFrame
import os

model_name = {
    'Conv. AE':'c_ae_model',
    'Dilated AE': 'dil_ae_model',
    'Latent Vec. AE': 'lat_ae_model'
}

class PageManager(Frame):
    def __init__(self, master, client, pred_mode, width=600, height=400):
        Frame.__init__(self, master, width=width, height=height)
        self.pred_mode = pred_mode
        if self.pred_mode not in pred_modes:
            raise ValueError('Invalid prediction mode!s')
        self.client = client
        self.is_pred_pending = False
        self.pred_data = None

    def on_prediction_received(self, prediction, chrom):
        raise RuntimeError('On prediction undefined')


class ImageUploadPageManager(PageManager):
    def __init__(self, master, queue, client, pred_mode='single_image'):
        PageManager.__init__(self, master, client, pred_mode)
        # define default widget images
        self.source_img = ImageFrame(self,
                                     E,
                                     os.path.join(os.getcwd(),
                                                  'images',
                                                  'icons',
                                                  'upload_logo_small.png'))
        # generate model output canvas/frame
        self.output_img = OutputFrame(self,
                                      W,
                                      os.path.join(os.getcwd(),
                                                   'images',
                                                   'icons',
                                                   'blank.png'))
        model_dropd_label = Label(master)
        model_dropd_label.configure(text='Model:')
        model_dropd_label.place(relx=0.19,
                                rely=0.795,
                                anchor=N)
        # reference to threading queue
        self.input_queue = queue
        # add button for configuring images
        choose_file = Button(self.source_img.canvas,
                             text='Choose File',
                             command=lambda: self.load_img())
        choose_file.place(relx=0.5,
                          rely=0.82,
                          anchor=N)
        self.tk_model_dir = StringVar(master)
        choices = {list(model_name.keys())[0],
                   list(model_name.keys())[1],
                   list(model_name.keys())[2]}
        self.tk_model_dir.set('Conv. AE')
        self.tk_model_dir.trace('w', self.on_new_model_selected)

        self.model_toggle = OptionMenu(self.source_img.canvas, self.tk_model_dir, *choices)
        self.model_toggle.place(relx=0.5,
                                rely=0.8915,
                                anchor=N)
        self.cur_img_path = ''

    def load_img(self):
        self.cur_img_path = askopenfilename(initialdir=os.getcwd(),
                                   filetypes=(("PNG File", "*.png"),
                                              ("All Files", "*.*")),
                                   title='Choose an Image')
        self.add_img_to_queue()

    def on_new_model_selected(self, *kwargs):
        self.add_img_to_queue()

    def add_img_to_queue(self):
        if len(self.cur_img_path) is 0:
            return
        if os.path.isfile(self.cur_img_path):
            try:
                # adjust image to fit to canvas
                img_source = load_to_canvas(self.cur_img_path,
                                            (self.source_img.frame_dim-5))
                # add image to the queue
                self.input_queue.put((img_source,
                                      model_name[self.tk_model_dir.get()]))
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
        self.pred_data = prediction_data

    def update_brightness(self, incrementing):
        self.pred_data.update_brightness(incrementing)
        self.output_img.on_output_generated(prediction_data=self.pred_data)