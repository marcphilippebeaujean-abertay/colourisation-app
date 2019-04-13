from keras.models import model_from_json
from img_processing import prepare_for_prediction, process_net_output, generate_chrominance
from threading import Thread
from prediction_data import PredictionData
from time import sleep
import os
import numpy as np

# used to identify and store real model names to be displayed,
# based on name of model folder that is used by thread to load
# in the model for predictions
true_model_names = {
    'c_ae_model': 'Convolutional AE',
    'cont_ae_model': 'Contextual AE',
    'dil_ae_model': 'Dilated AE',
    'lat_ae_model': 'Latent Vec. AE'
}


def load_model(model_dir):
    model = None
    with open(os.path.join(model_dir, 'model.json'), 'r') as f:
        json_info = f.read()
        model = model_from_json(json_info)
    weights_path = os.path.join(model_dir, 'weights.h5')
    if os.path.isfile(weights_path):
        model.load_weights(weights_path)
    return model


def generate_prediction(input_img, model_name='c_ae_model', label=None):
    model_path = os.path.join(os.getcwd(), 'model_info', model_name)
    model = load_model(model_path)
    pp_img = np.asarray(prepare_for_prediction(input_img))
    img_rows, img_cols = pp_img.shape[0], pp_img.shape[1]
    # reshaping required to meet input requirements for predictions
    net_input = np.empty((1, img_rows, img_cols, 1))
    # assign luminance channel of image as input
    net_input[0] = pp_img[..., :1]
    # normalise channels
    net_input /= 100
    # generate prediction
    if model_name == 'cont_ae_model':
        label_reshaped = np.empty((1, len(label)))
        label_reshaped[0] = label
        net_input = [net_input, label_reshaped]
    pred = model.predict(net_input)
    ground_truth = None if pp_img.shape[2] < 2 else pp_img[..., 1:]
    final_pred = PredictionData(input_img,
                                pred,
                                true_model_names[model_name])
    return final_pred


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
                        if model_dir == 'cont_ae_model':
                            self.__put_pred(model_dir, img, queue_data[2])
                        else:
                            self.__put_pred(model_dir, img)
                else:
                    # queue data 1 determines the model if it is predefined
                    self.__put_pred(queue_data[1], img)
            else:
                sleep(0.1)

    def __put_pred(self, model_name, input_img, label=None):
        pred = generate_prediction(model_name=model_name,
                                   input_img=input_img,
                                   label=label)
        self.output_queue.put(pred)