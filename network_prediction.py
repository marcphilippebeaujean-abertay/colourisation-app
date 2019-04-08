from keras.models import model_from_json
from img_processing import prepare_for_prediction, process_net_output, generate_chrominance
from threading import Thread
from time import sleep
import os
import numpy as np


def load_model(model_dir):
    model = None
    with open(os.path.join(model_dir, 'model.json'), 'r') as f:
        json_info = f.read()
        model = model_from_json(json_info)
    weights_path = os.path.join(model_dir, 'weights.h5')
    if os.path.isfile(weights_path):
        model.load_weights(weights_path)
    return model


def generate_prediction(input_img, model_name='c_ae_model'):
    model_path = os.path.join(os.getcwd(), 'model_info', model_name)
    model = load_model(model_path)
    pp_img = np.asarray(prepare_for_prediction(input_img))
    img_rows, img_cols = pp_img.shape[0], pp_img.shape[1]
    # reshaping required to meet input requirements for predictions
    net_input = np.empty((1, img_rows, img_cols, 1))
    # assign luminance channel of image as input
    net_input[0] = pp_img[..., :1]
    # normalise input
    net_input /= 100
    # generate prediction
    pred = model.predict(net_input)
    # generate chrominance
    output = process_net_output(pred, input_img)
    chrom = generate_chrominance(pred, input_img)
    return output, chrom


class PredictionThread(Thread):
    def __init__(self, input_queue, output_queue):
        super().__init__()
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.multi_pred = False
        self.model_dirs = os.listdir(os.path.join(os.getcwd(), 'model_info'))

    def run(self):
        while True:
            # check if queue contains a new prediction to make
            if self.input_queue.empty() is False:
                queue_data = self.input_queue.get()
                img = queue_data[0]
                if self.multi_pred:
                    for model_dir in self.model_dirs:
                        self.__put_pred(model_dir, img)
                else:
                    self.__put_pred(queue_data[1], img)
            else:
                sleep(0.1)

    def __put_pred(self, model_name, input_img):
        pred = generate_prediction(model_name=model_name,
                                   input_img=input_img)
        self.output_queue.put(pred)