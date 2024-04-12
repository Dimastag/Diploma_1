from moviepy.editor import VideoFileClip
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog as fd
from datetime import timedelta

SAVING_FRAMES_PER_SECOND = 1

def format_timedelta(td):
    result = str(td)

    try:
        result, ms = result.split(".")
    except ValueError:
        return result + ".00".replace(":", "-")

    ms = round(int(ms) / 10000)
    return f"{result}.{ms:02}".replace(":", "-")

def extract_frames(video_file, output_folder):
    video_clip = VideoFileClip(video_file)
    filename, _ = os.path.splitext(video_file)

    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    saving_frames_per_second = min(video_clip.fps, SAVING_FRAMES_PER_SECOND)
    step = 1 / video_clip.fps if saving_frames_per_second == 0 else 1 / saving_frames_per_second

    for current_duration in np.arange(0, video_clip.duration, step):
        frame_duration_formatted = format_timedelta(timedelta(seconds=current_duration)).replace(":", "-")
        frame_filename = os.path.join(output_folder, f"frame_{filename}_{frame_duration_formatted}.jpg")

        video_clip.save_frame(frame_filename, current_duration)

def select_video_file():
    video_file = fd.askopenfilename(title="Select a Video File")
    return video_file

def select_output_folder():
    output_folder = fd.askdirectory(title="Select Output Folder")
    return output_folder

def process_video():
    video_file = select_video_file()
    if video_file:
        output_folder = select_output_folder()
        if output_folder:
            extract_frames(video_file, output_folder)

# Создание интерфейса Tkinter
root = tk.Tk()
root.title("Video Frame Extractor")

process_button = tk.Button(root, text="Process Video", command=process_video)
process_button.pack()

root.mainloop()