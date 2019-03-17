from keras.models import model_from_json
from img_processing import prepare_for_prediction
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


def generate_prediction(input_img, model_name='c_ae_model'):
    model_path = os.path.join(os.getcwd(), 'model_info', model_name)
    model = load_model(model_path)
    #input_img = prepare_for_prediction(input_img)
    print('loaded model')

