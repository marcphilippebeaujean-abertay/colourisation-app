from keras.models import model_from_json
from img_processing import prepare_for_prediction, process_net_output
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
    prepd_img = np.asarray(prepare_for_prediction(input_img))
    img_rows, img_cols = prepd_img.shape[0], prepd_img.shape[1]
    # reshaping required to meet input requirements for predictions
    net_input = np.empty((1, img_rows, img_cols, 1))
    net_input[0, :] = prepd_img[..., :1]
    pred = model.predict(net_input)
    return pred
