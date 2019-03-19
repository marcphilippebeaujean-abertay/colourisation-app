import cv2
import numpy as np
from PIL import ImageTk, Image


def fit_to_canvas(img, max_dim):
    # retrieve image dimensions
    height, width = img.shape[:2]
    # rescale image if appropriate, to fit canvas
    ratio = min(max_dim / width, max_dim / height)
    width *= ratio
    height *= ratio
    return cv2.resize(img,
                      (int(width), int(height)),
                      interpolation=cv2.INTER_CUBIC)


def load_to_canvas(file_path, max_dim):
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


def prepare_for_prediction(img, pred_dim=(32, 32)):
    if not isinstance(pred_dim, tuple):
        raise TypeError('dimensions was not a tuple')
    # sample image to network input
    img = cv2.resize(img, pred_dim, interpolation=cv2.INTER_CUBIC)
    # convert image to lab
    img = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    return img


def denormalize_channel(min_val, max_val, channel_val):
    channel_val *= (min_val+max_val)
    channel_val -= min_val


def process_net_output(net_output, net_input, original_image):
    # initialise array
    img_shape = (net_output.shape[1],
                 net_output.shape[2],
                 3)
    final_output = np.zeros(img_shape)
    final_output = final_output.astype(np.float32)
    # concatenate luminance values and denormalize
    final_output[..., :1] = net_input[..., :1]
    denormalize_channel(0, 100, final_output[..., :1])
    # add network output predictions to image
    final_output[..., 1:] = net_output
    denormalize_channel(127, 128, final_output[..., 1:2])
    denormalize_channel(128, 127, final_output[..., 2:])
    # scale up image
    final_output = cv2.resize(final_output,
                              (original_image.shape[1],
                               original_image.shape[0]))
    final_output[..., :1] = cv2.cvtColor(original_image,
                                         cv2.COLOR_RGB2LAB)[..., :1]
    final_output = cv2.cvtColor(final_output, cv2.COLOR_LAB2RGB)
    print(final_output.shape)
    return cv2_to_tk_img(np.uint8(final_output))


def cv2_to_tk_img(img):
    img = Image.fromarray(img)
    return ImageTk.PhotoImage(img)




