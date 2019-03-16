from tkinter import *
from keras.models import model_from_json
from image_frame import ImageFrame
from threading import Thread
import os


def load_model(model_dir):
    model = None
    with open(os.path.join(model_dir, 'model.json'), 'r') as f:
        json_info = f.read()
        model = model_from_json(json_info)
    weights_path = os.path.join(model_dir, 'weights.h5')
    if os.path.isfile(weights_path):
        model.load_weights(weights_path)
    return model


class PredictionThread(Thread):
    def __init__(self, model_path):
        super().__init__()
        self.model_path = model_path
        self.model = None

    def run(self):
        self.model = load_model(self.model_path)


class ModelOutputManager:
    def __init__(self, master=None):
        self.master = master
        # generate model output canvas/frame
        self.output_img = ImageFrame(self.master,
                                     W,
                                     os.path.join(os.getcwd(), 'eye_logo.png'))

    def generate_prediction(self, input_img, model_name='c_ae_model'):
        # load in keras model for prediction
        self.output_img.init_animation(self.output_img.loading_anim().__next__)
        model_path = os.path.join(os.getcwd(), 'model_info', model_name)
        model = load_model(model_dir=model_path)

