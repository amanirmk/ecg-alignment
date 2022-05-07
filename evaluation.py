import numpy as np

def analyze_deviation(tensor):
    """ Compares the values of pixels by frame across videos and returns a measure indicating the variability """
    std_by_frame = np.std(tensor, axis=0)
    std_overall = np.mean(std_by_frame, axis=0)
    std_overall = crop_image(std_overall)
    return np.mean(std_overall)

def crop_image(img):
    """ Takes an ECG image and removes everything except the heart """
    img[:, :200] = 0
    img[:, 800:] = 0
    img[:95, :] = 0
    img[600:, :] = 0
    img[90:120, 550:600] = 0
    return img