import cv2
import numpy as np
import os
from video_alignment import align_videos

def data_to_tensor(fnames, num_frames=20, sec_per_cycle=2, grayscale=True):
    """ Description: Transforms raw DICOM data into a tensor of synchronized videos
        Input: Filenames of DICOM data, the number of frames to use in the tensor, the number of seconds for a heart cycle, and a boolean for grayscale
        Output: A tensor of dimensions (number of videos, number of frames, height of video, width of video, 1 or 3 channels depending on grayscale)
    """
    vid_names = [f"v{i}" for i in range(len(fnames))]
    align_videos(fnames, sec_per_cycle, vid_names)
    tensor = create_tensor([f"{n}.avi" for n in vid_names], num_frames, grayscale)
    for name in vid_names:
        os.remove(f"./{name}.avi")
    return tensor


def create_tensor(fnames, num_frames, grayscale=True):
    """ Description: Samples frames from videos to create a tensor
        Input: Filenames of videos (should be aligned and trimmed), the number of frames to use in the tensor, and a boolean for grayscale
        Output: A tensor of dimensions (number of videos, number of frames, height of video, width of video, 1 or 3 channels depending on grayscale)
    """
    videos = []
    for fname in fnames:
        vid = cv2.VideoCapture(fname)

        # find the length of the video in milliseconds
        cont = True
        length = 0
        while cont:
            length = vid.get(cv2.CAP_PROP_POS_MSEC)
            cont, _ = vid.read()

        # sample frames
        frames = []
        for msec in np.linspace(0, length, num_frames):
            vid.set(cv2.CAP_PROP_POS_MSEC, msec)
            _, frame = vid.read()
            if grayscale:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            frames.append(frame)
        videos.append(frames)

    return np.asarray(videos)