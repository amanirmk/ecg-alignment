from video_alignment import align_videos

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
video_names=[f"video{i}" for i in range(len(video_paths))]

align_videos(video_paths, 2, video_names)