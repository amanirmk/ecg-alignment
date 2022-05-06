import numpy as np
import cv2

def find_beats(video):
    """ Description: Returns a list of frames where beats start in the video
        Input: A video (sequence of RGB images)
        Output: A list containing the indices of frames in the video that are the start of a heartbeat
    """
    signal_height = find_signal_height(video)
    beats = [i for i in range(len(video)) if is_beat(video[i], signal_height)]
    
    # condense nearby beats into first one
    i = 1
    last_frame = beats[0]
    while i < len(beats):
        if beats[i] - last_frame < 2:
            last_frame = beats[i]
            del beats[i]
        else:
            last_frame = beats[i]
            i += 1

    return beats


def find_signal_height(video):
    """ Description: Finds the typical height of heartbeat spike for a video (Helper for find_beats)
        Input: A video (sequence of RGB images)
        Output: An integer number of pixels indicating the typical height of a heartbeat peak
    """
    pcts = []
    for img in video:
        mask = signal_mask(img)
        x, _, _ = locate_line(mask)
        mask[:, x-4:x+4] = 0  # remove vertical line for location in signal
        ys, _ = np.where(mask > 0)
        y = np.median(ys) # use median y-position of pixels for baseline of signal
        pcts.append(max(abs(y - np.percentile(ys, 5)), abs(y - np.percentile(ys, 95)))) # use highest and lowest 5% marks for height
    signal_height = int(np.mean(pcts))
    return signal_height 


def is_beat(img, signal_height=None):
    """ Description: Returns True if image contains a beat and False otherwise (Helper for find_beats)
        Input: An RGB image and an optional height for typical heartbeat peak in pixels
        Output: True if frame overlaps with a heartbeat and False otherwise
    """
    mask = signal_mask(img)
    x, y, h = locate_line(mask)
    mask = mask//255

    # remove any extra of vertical line
    end = x
    while np.sum(mask[y-h:y+h, end]) == 2*h and end > 0:
        end -= 1

    # look at region to left of vertical green line
    target = mask[y-h:y+h, end-5:end]

    # if vertical variance of horizontal line exceeds threshold, consider it a beat
    ys, _ = np.where(target > 0)
    is_a_beat = np.var(ys) > 5

    # require line to also be a certain percentage of typical peak height if provided
    if signal_height is not None:
        is_a_beat = is_a_beat and (np.sum(target[:h-int(0.5*signal_height),:]) > 0 or np.sum(target[h+int(0.5*signal_height):,:]) > 0) 

    return is_a_beat


def signal_mask(img):
    """ Description: Returns mask containing only the green heartbeat signal (Helper for is_beat)
        Input: An RGB image 
        Output: A binary image containing the heartbeat signal
    """
    mask = cv2.inRange(cv2.cvtColor(img, cv2.COLOR_RGB2HSV), (30, 10, 50), (90, 255, 255))  # filter for green signal
    mask[:600,:] = 0 # remove all noise clearly from above the signal
    return mask


def locate_line(mask):
    """ Description: Returns coordinates of current location in signal (Helper for is_beat)
        Input: A binary image containing heartbeat signal (output of signal_mask)
        Output: X and Y coordinates of signal, as well as the signal's height
    """
    mask = np.array(mask)

    # find the y position of the horizontal green signal
    ys, _ = np.where(mask[:,:] > 0)
    y = int(np.median(ys))

    # remove the horizontal line, leaving just the top of the vertical green line
    mask[650:,:] = 0

    # identify the line (approximately)
    contours, _ = cv2.findContours(mask.astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    x,_,w,h = max([cv2.boundingRect(c) for c in contours], key=lambda b: b[3])

    # remove all noise from outside the relevant area
    mask[:, x+w:] = 0
    mask[:, :x-w] = 0

    # find the x position of the vertical green signal
    _, xs = np.where(mask[:,:] > 0)
    x = int(np.mean(xs))

    return x, y, h