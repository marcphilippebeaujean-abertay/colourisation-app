import cv2


def fit_to_canvas(img, max_dim):
    # retrieve image dimensions
    height, width = img.shape[:2]
    # rescale image if appropriate, to fit canvas
    ratio = min(max_dim / width, max_dim / height)
    width *= ratio
    height *= ratio
    return cv2.resize(img, (int(width), int(height)), interpolation=cv2.INTER_CUBIC)


def get_pre_processed_img(file_path, max_dim):
    # load image
    img = cv2.imread(file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # fit image to canvas
    img = fit_to_canvas(img, max_dim)
    # generate lab version
    lab_img = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    # return all versions
    return img, lab_img


