#!/usr/bin/python3

"""Usage:

./record_copulation_assay.py <lens position> <path/to/save/directory>
"""

from picamera2 import Picamera2
from libcamera import controls
import cv2
import os, sys
from datetime import datetime




def record_video(cam_obj, dur, fps, lens_position, output_name):
    """
    Function uses Picamera2 to record a video with a given duration, framerate, and lens focus.
    The image size is hard-coded to be a square of the largest possible size (1296x1296) for the 
    Raspberry Pi Camera Module 3 and hardcoded to record at 30 fps.

    :param cam_obj: instance of Picamera2()
    :param dur: duration of recording in seconds
    :param fps: recording framerate in frames per second
    :param lens_position: value used to set lens focus, units of diopters = 1/distance in meters
    :param output_name: name of output video, include path if not saving to current directory, include the file extension

    :type cam_obj: Picamera2
    :type dur: float
    :type fps: float
    :type lens_position: float
    :type output_name: str
    """

    #configure video
    vid_config = cam_obj.create_video_configuration(main={"size":(1296, 1296)}, controls={"FrameRate":fps})
    cam_obj.configure(vid_config)

    #set camera controls
    cam_obj.set_controls({"AfMode":controls.AfModeEnum.Manual, "LensPosition":lens_position})

    #record video
    cam_obj.start_and_record_video(output_name, duration=dur)




def merge_videos(continuous_video, timelapse_video, final_output):
    """
    Function uses OpenCV to stream through the 30-min 30 fps video and grab every 30th frame (1 fps)
    and prepend these frames to the 11.5-hr 1 fps video to output a 12-hr 1 fps video.

    :param continuous_video: path to 30-min video
    :param timelapse_video: path to 11.5-hr video
    :param final_output: name or path to output video, include the file extension

    :type continuous_video: str
    :type timelapse_video: str
    :type final_output: str
    """

    #open final output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    vid_out = cv2.VideoWriter(final_output, fourcc, 30.0, (1296, 1296))


    #opening 30-min video and iterate through video frames
    cap_continuous = cv2.VideoCapture(continuous_video)
    if not cap_continuous.isOpened():
        raise FileNotFoundError(f"Could not open {continuous_video}")

    frame_counter = 0
    while cap_continuous.isOpened():
        ret, frame  = cap_continuous.read()
        if not ret:
            break
        if (frame_counter % 30) == 0:
            #add frame to new video
            vid_out.write(frame)
        frame_counter += 1
    cap_continuous.release()


    #opening 11.5-hr video and iterate through video frames
    cap_timelapse = cv2.VideoCapture(timelapse_video)
    if not cap_timelapse.isOpened():
            raise FileNotFoundError(f"Could not open {timelapse_video}")

    while cap_timelapse.isOpened():
        ret, frame  = cap_timelapse.read()
        if not ret:
            break
        #add frame to new video
        vid_out.write(frame)
    cap_timelapse.release()


    vid_out.release()



def get_timestamp():
    """
    Function uses the datetime module to return a timestamp string to be used
    in the filename for an output video file. The format is "M-D-Y_H.M.S"

    :returns: timestamp string
    :rtype: str
    """

    timestamp = datetime.now().strftime("%x_%X").replace("/", "-").replace(":", ".")

    return timestamp



def get_output_video_names(path_to_save_dir):
    """
    Function uses the get_timestamp() function to return a timestamp string to be 
    used in the filename for the output video files. The format is "M-D-Y_H.M.S" 
    The function then returns path names for the 30-min, intermediate 11.5-hr, and 
    the final 12-hr video. Note that this function will create the directory for
    the path you input if it does not already exist and will also create a subdiretory
    called "intermediate_timelapse_videos" (unless it already exists) to save the 
    11.5-hr timelapse video inside.

    :param path_to_save_dir: path to directory you want to save videos inside
    :type path_to_save_dir: str

    :returns: path names for the 30-min, intermediate 11.5-hr, and the final 12-hr video
    :rtype: (str, str, str)
    """

    #create directories if they dont already exist
    os.makedirs(os.path.join(path_to_save_dir, "intermediate_timelapse_videos"), exist_ok=True)

    #get timestamp for filenames
    timestr = get_timestamp()

    #generate output file paths
    out_30min = os.path.join(path_to_save_dir, f"{timestr}_30min_continous.mp4")
    out_intermediate = os.path.join(path_to_save_dir, "intermediate_timelapse_videos", f"{timestr}_11.5hr_timelaspe.h264")
    out_12hr = os.path.join(path_to_save_dir, f"{timestr}_12hr_timelapse.mp4")

    return out_30min, out_intermediate, out_12hr




def record_and_process_videos(save_path, lp):
    """
    Function records a 30-min, 30fps video and saves it to the save_path directory
    then records a 11.5-hr, 1fps timelapse and saves it to the save_path/intermediate_timelapse_videos
    directory. Finally, the function takes every 30th frame from the 30-min video and prepends them to
    the timelapse video to output a final 12-hr, 1fps timelapse saved to the save_path directory. Note
    that if the save_path directory does not exist yet, it will be created.

    :param save_path: path to directory you want to save videos inside
    :param lp: value used to set lens focus, units of diopters = 1/distance in meters

    :type save_path: str
    :type lp: float
    """

    #initializing Picamera2 object
    picam = Picamera2()

    #get output names
    name_30, name_inter, name_12 = get_output_video_names(save_path)

    #record 30-min video
    record_video(picam, 1800, 30, lp, name_30)

    #record intermediate timelaspe
    record_video(picam, 41400, 1, lp, name_inter)

    #output final 12 hour timelapse
    merge_videos(name_30, name_inter, name_12)

    #turn off camera
    picam.close()







def main():

    #parsing command line arguments
    if len(sys.argv) < 3:
        print("Usage: ./record_copulation_assay.py <lens position> <path/to/save/directory>")
        sys.exit(1)
    lens_pos = float(sys.argv[1])
    savepath = str(sys.argv[2])

    #run recordings and processing
    record_and_process_videos(savepath, lens_pos)






if __name__ == "__main__":
    main()





