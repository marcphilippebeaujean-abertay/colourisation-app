import cv2
import numpy as np


def fit_to_canvas(img, max_dim):
    # retrieve image dimensions
    height, width = img.shape[:2]
    # rescale image if appropriate, to fit canvas
    ratio = min(max_dim / width, max_dim / height)
    width *= ratio
    height *= ratio
    return cv2.resize(img, (int(width), int(height)), interpolation=cv2.INTER_CUBIC)


def prepare_for_prediction(img, pred_dim):
    if not isinstance(pred_dim, tuple):
        raise TypeError('dimensions was not a tuple')
    # convert image to lab
    img = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    # resize to fit network input
    img = cv2.resize(img, (pred_dim[0], pred_dim[1]), interpolation=cv2.INTER_CUBIC)
    return img


def get_pre_processed_img(file_path, max_dim):
    # load image and extract alpha channel
    img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    alpha = img[:,:,3]
    # make colour conversion
    out_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # add alpha information after conversions
    out_img = np.dstack([out_img, alpha])
    # fit image to canvas
    out_img = fit_to_canvas(out_img, max_dim)
    # return all versions
    return out_img
