from data_processing import data_to_tensor
from video_alignment import align_videos

# This example requires the echocardiogram data follow the same structure as our provided data.

data_path = './data'

patients = ["10026_20171208", 
            "10651_20171118", 
            "14369_20180420", 
            "15751_20180728", 
            "20198_20180511", 
            "20218_20171201", 
            "20596_20171118", 
            "21104_20180322", 
            "22444_20180404"]

indices = [["02", "03", "04"],
           ["02", "03"],
           ["41", "42"],
           ["02", "03"],
           ["03", "04"],
           ["02", "05", "06", "07"],
           ["02", "03"],
           ["02", "03", "04"],
           ["02", "03", "04"]]

video_paths = sum([[f"{data_path}/{patients[i]}/IM-0001-00{index}.dcm" for index in indices[i]] for i in range(len(patients))], [])
names = [f"video-{i}" for i in range(len(video_paths))] # to make sure names are unique

align_videos(video_paths, 2) # save to computer
X = data_to_tensor(video_paths) # obtain tensor for decomposition