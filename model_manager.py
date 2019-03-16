from tkinter import *
from keras.models import model_from_json
from image_frame import ImageFrame
import os


def load_model(model_dir):
    model = None
    with open(model_dir, 'r') as f:
        json_info = f.read()
        model = model_from_json(json_info)
    return model


class ModelOutputManager:
    def __init__(self, master=None):
        self.master = master
        # generate model output canvas/frame
        self.output_img = ImageFrame(self.master,
                                     W,
                                     os.path.join(os.getcwd(), 'eye_logo.png'))

    def generate_prediction(self, input_img, model_file='c_ae_model.json'):
        # load in keras model for prediction
        self.output_img.init_animation(self.output_img.loading_anim().__next__)
        model = load_model(os.path.join(
            os.getcwd(),
            model_file))

