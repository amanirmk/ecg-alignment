# Automatic Alignment of Echocardiogram Sequences

This repository contains an algorithm for aligning a specific view of echocardiogram videos based on the heart signal. Note: This repository does not contain the data required to run the code, due to privacy concerns.

The algorithm is composed fundamentally of three steps: (1) identify which part of the signal a frame corresponds to, (2) determine whether the frame contains the start of a heartbeat, (3) segment video by complete heartbeat cycles and normalize. All code pertaining to step 1 and 2 are in `beat_identification.py`. Step 3 is in `cycle_normalization.py` and `video_alignment.py`. The file `data_processing.py` provides methods for converting the videos into data. `evalutation.py` contains a heuristic for evaluating the synchronization.

For purposes that involve tensor techniques, use `X = data_to_tensor(dicom_file_names)` to obtain the tensor. For generating the aligned videos, use `align_videos(dicom_file_names, seconds_per_heartbeat_cycle)`.

For questions, email amainakilaas@hmc.edu.
