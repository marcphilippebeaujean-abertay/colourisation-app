import skimage
import cv2
import numpy as np


def normalise_channel(min_val, max_val, channel_vals):
    channel_vals += min_val
    channel_vals /= (min_val+max_val)


def denormalize_channel(min_val, max_val, channel_val):
    channel_val *= (min_val+max_val)
    channel_val -= min_val


def get_processed_data(img_data):
    img_data = np.asarray(img_data)
    lab_img = np.empty(img_data.shape, dtype=np.float32)
    for i in range(0, len(img_data)):
        lab_img[i] = cv2.cvtColor(img_data[i], cv2.COLOR_RGB2LAB)
    lab_img[...,:1] /= 255
    lab_img[..., 1:] /= 255
    X_data = lab_img[...,:1]
    y_data = lab_img[...,1:]
    return X_data, y_data


def get_processed_data_skimage(img_data):
    img_data = np.asarray(img_data)
    lab_img = np.empty(img_data.shape)
    for i in range(0, len(img_data)):
        lab_img[i] = skimage.color.rgb2lab(img_data[i])
    lab_img[...,:1] /= 100
    normalise_channel(127, 128, lab_img[...,1:2])
    normalise_channel(128, 127, lab_img[...,2:])
    X_data = lab_img[...,:1]
    y_data = lab_img[...,1:]
    return X_data, y_data


def proc_output(net_input, net_output, ground_truth):
    img_shapes = (net_input.shape[0], net_input.shape[1], net_input.shape[1], 3)
    final_output = np.zeros(img_shapes)
    final_output = final_output.astype(np.float32)
    # Concatenate luminance values and denormalize
    final_output[..., :1] = net_input
    denormalize_channel(0, 100, final_output[..., :1])
    final_output[..., 1:] = net_output
    denormalize_channel(127, 128, final_output[..., 1:2])
    denormalize_channel(128, 127, final_output[..., 2:])
    final_output = final_output.astype(np.float32)
    # Concatenate and denormalize ground truth
    final_ground_truth = np.zeros(img_shapes)
    final_ground_truth[..., :1] = final_output[..., :1]
    final_ground_truth[..., 1:] = ground_truth
    denormalize_channel(127, 128, final_ground_truth[..., 1:2])
    denormalize_channel(128, 127, final_ground_truth[..., 2:])
    final_ground_truth = final_ground_truth.astype(np.float32)
    # Convert final output to rgb
    for i in range(len(final_output)):
        final_output[i] = cv2.cvtColor(final_output[i], cv2.COLOR_LAB2RGB)
    for i in range(len(final_ground_truth)):
        final_ground_truth[i] = cv2.cvtColor(final_ground_truth[i], cv2.COLOR_LAB2RGB)
    return final_output, final_ground_truth
