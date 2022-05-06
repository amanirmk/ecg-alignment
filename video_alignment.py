import time
import os
from pydicom import dcmread
from cycle_normalization import normalize

def align_videos(fnames, sec_per_cycle, names=[]):
    """ Description: Normalizes and trims videos to same length
        Input: List of video paths, the number of seconds a cycle should last, and a list of names to save the videos as
        Output: None, saves the set of normalized and trimmed videos to computer
    """
    if len(names) != len(fnames):
        names = [fname.split('/')[-1].split('.')[0] for fname in fnames]
    min_cycle_count = normalize_videos(fnames, sec_per_cycle, names)
    min_secs = min_cycle_count * sec_per_cycle
    trim_videos(names, min_secs)
    

def normalize_videos(fnames, sec_per_cycle, names=[]):
    """ Description: Normalizes a set of videos
        Input: List of video paths, the number of seconds a cycle should last, and a list of names to save the videos as
        Output: Returns the number of cycles in the shortest video and saves the normalized videos to computer
    """
    if len(names) != len(fnames):
        names = [fname.split('/')[-1].split('.')[0] for fname in fnames]
    num_cycles = []
    for fname, name in zip(fnames, names):
        video = load_video(fname)
        cycle_count = normalize(video, sec_per_cycle, name)
        num_cycles.append(cycle_count)
    return min(num_cycles)


def trim_videos(names, sec, delete_old=True):
    """ Description: Trims a set of videos to a specified integer number of seconds
        Input: A list of video names, the number of seconds to trim to, and an optional boolean to indicate deleting the old videos
        Output: None, saves trimmed videos to computer
    """
    max_time = time.strftime('%H:%M:%S', time.gmtime(sec))
    for name in names:
        os.system(f"ffmpeg -i {name}.avi -ss 00:00:00 -t {max_time} -c:v copy -c:a copy {name}_trimmed.avi")
        if delete_old:
            os.remove(f"./{name}.avi")
            os.system(f"mv ./{name}_trimmed.avi ./{name}.avi")


def load_video(fname):
    """ Description: Loads a video from a filename
        Input:  The filename of a video (string)
        Output: The video (sequence of RGB images)
    """
    video = [img for img in dcmread(fname).pixel_array]
    return video