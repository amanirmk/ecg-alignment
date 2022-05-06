import cv2
import os
from beat_identification import find_beats

def normalize(video, sec_per_cycle, name):
    """ Description: Sets each cycle in a heartbeat video to the same length
        Input: A video (sequence of RGB images), the number of seconds per heartbeat cycle, and a name to save to
        Output: Returns the number of heart cycles in the normalized video, saves video to computer
    """
    beats = find_beats(video)
    beat_videos = split_video(video, beats)

    # write out individual cycle videos
    for i in range(len(beat_videos)):
        vid = beat_videos[i]
        num_frames = len(vid)
        fps = num_frames / sec_per_cycle
        write_video(f"./{name}-{i}.avi", vid, fps)

    # combine into single video
    vids = "|".join([f"./{name}-{i}.avi" for i in range(len(beat_videos))])
    os.system(f"ffmpeg -i 'concat:{vids}' -c copy ./{name}.avi")

    # delete old individual videos
    for i in range(len(beat_videos)):
        os.remove(f"./{name}-{i}.avi")
    
    return len(beat_videos)


def split_video(video, beats):
    """ Description: Splits video into segments each containing a single heart beat cycle (Helper for normalize_cycles)
        Input: A video (sequence of RGB images) and a list of beats (output of find_beats)
        Output: A list of videos, each video containing a single complete heartbeat cycle
    """
    beat_videos = []
    for i in range(1, len(beats)):
        beat_videos.append(video[beats[i-1]:beats[i]])
    return beat_videos


def write_video(fname, video, fps):
    """ Description: Saves a video to file with a given fps
        Input: Filename, a video (sequence of RGB images), and an fps
        Output: None, saves video to computer
    """
    h,w = video[0].shape[:2] 
    fourcc = cv2.VideoWriter.fourcc(*'MJPG')
    out = cv2.VideoWriter(fname, fourcc, fps, (w, h))
    for img in video:
        out.write(img)
    out.release()
    cv2.destroyAllWindows()