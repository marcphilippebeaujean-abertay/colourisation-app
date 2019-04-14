import cv2
import numpy as np
from skimage.color import rgb2lab
from PIL import ImageTk, Image


def add_alpha(out_img, original_img):
    try:
        if original_img.shape[2] > 3:
            alpha = original_img[:, :, 3]
            out_img = np.dstack([out_img, alpha])
        return out_img
    except:
        return out_img


def fit_to_canvas(img, max_dim):
    # retrieve image dimensions
    height, width = img.shape[:2]
    if height > max_dim or width > max_dim:
        # rescale image if appropriate, to fit canvas
        ratio = min(max_dim / width, max_dim / height)
        width *= ratio
        height *= ratio
        img = cv2.resize(img, (int(width), int(height)), interpolation=cv2.INTER_CUBIC)
    return img


def load_to_canvas(file_path, max_dim):
    # load image and extract alpha channel
    img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
    # make colour conversion
    out_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # add alpha information after conversions
    out_img = add_alpha(out_img, img)
    # fit image to canvas
    out_img = fit_to_canvas(out_img, max_dim)
    # return final version
    return out_img


def prepare_for_prediction(img, pred_dim=(32, 32)):
    if not isinstance(pred_dim, tuple):
        raise TypeError('dimensions was not a tuple')
    # sample image to network input
    img = cv2.resize(img, pred_dim, interpolation=cv2.INTER_CUBIC)
    # convert image to lab
    img = rgb2lab(img[..., :3])
    return img


def denormalize_channel(min_val, max_val, channel_val):
    channel_val *= (min_val+max_val)
    channel_val -= min_val


def process_net_output(net_output, original_image, target_size=None):
    # initialise array
    img_shape = (net_output.shape[1], net_output.shape[2], 3)
    final_output = np.zeros(img_shape)
    final_output = final_output.astype(np.float32)
    # add network output predictions to image
    final_output[..., 1:] = net_output
    # denormalize the channels
    denormalize_channel(128, 127, final_output[..., 1:2])
    denormalize_channel(127, 128, final_output[..., 2:])
    # scale up chrominance output from network to original size
    final_out_res = target_size
    if target_size is None:
        final_out_res = original_image.shape[:2][::-1]
    final_output = cv2.resize(final_output,
                              final_out_res)
    if final_output.shape != original_image.shape:
        if target_size != None:
            original_image = cv2.resize(original_image,
                                        target_size)
    fin_output_lab = cv2.cvtColor(original_image[..., :3],
                                  cv2.COLOR_RGB2LAB)
    fin_output_lab = fin_output_lab.astype(np.float32)
    # processing required by OpenCV to convert the 8bit images
    # back into the real LAB colourspace values
    fin_output_lab[..., :1] /= 255
    fin_output_lab[..., :1] *= 100
    # use luminance from original image
    final_output[..., :1] = fin_output_lab[..., :1]
    final_output = cv2.cvtColor(final_output,
                                cv2.COLOR_LAB2RGB)
    # denormalize rgb output (will be in range 0 - 1)
    final_output *= 255
    # apply alpha channel if necessary
    if target_size is None:
        final_output = add_alpha(final_output, original_image)
    return cv2_to_tk_img(np.uint8(final_output))

def process_set_output(normed_output):
    final_output = np.zeros(normed_output.shape)
    # create copy of output array (should contain luminance
    # and predicted chrominance from network
    final_output = normed_output
    denormalize_channel(0, 100, final_output[..., :1])
    denormalize_channel(127, 128, final_output[..., 1:2])
    denormalize_channel(128, 127, final_output[..., 2:])
    final_output = final_output.astype(np.float32)
    # Convert final output images to rgb
    for i in range(len(final_output)):
        img = final_output[i]
        final_output[i] = cv2.cvtColor(img, cv2.COLOR_LAB2RGB)
    return final_output

def cv2_to_tk_img(img):
    tk_img = Image.fromarray(np.uint8(img))
    return ImageTk.PhotoImage(tk_img)


def generate_chrominance(ab, input_img):
    out_img = np.ones((ab.shape[1], ab.shape[2], 3), dtype=np.float32)
    denormalize_channel(128, 127, ab[..., :1])
    denormalize_channel(127, 128, ab[..., 1:])
    out_img[..., :1] *= 50
    out_img[..., 1:] = ab
    out_img = cv2.cvtColor(out_img[..., :3],
                           cv2.COLOR_LAB2RGB)
    out_img *= 255
    out_img = cv2.resize(out_img, (input_img.shape[1], input_img.shape[0]))
    out_img = add_alpha(out_img, input_img)
    return cv2_to_tk_img(np.uint8(out_img))