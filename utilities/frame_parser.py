from moviepy.editor import VideoFileClip
import numpy as np
import os
import tkinter as tk
from tkinter import filedialog as fd
from datetime import timedelta

SAVING_FRAMES_PER_SECOND = 1

class FrameParser:

    def __init__(self, root):
        self.root = root
        self.total_frames = 0
        self.root.geometry('400x200')
        self.root.title("Video Frame Extractor")

        mode_label = tk.Label(self.root, text="Choose the time delta and video from your PC:")
        mode_label.pack()

        time_delta_button = tk.Button(root, text="Specify time delta", command=lambda: self.format_timedelta())
        time_delta_button.pack()

        process_button = tk.Button(root, text="Process Video", command=self.process_video)
        process_button.pack()

        exit_button = tk.Button(self.root, text="Exit", command=self.on_exit)
        exit_button.pack()


    def format_timedelta(self, td):
        result = str(td)
        try:
            result, ms = result.split(".")
        except ValueError:
            return result + ".00".replace(":", "-")
        ms = round(int(ms) / 10000)
        return f"{result}.{ms:02}".replace(":", "-")

    def extract_frames(self, video_file, output_folder):
        video_clip = VideoFileClip(video_file)
        filename, _ = os.path.splitext(video_file)
        video_file_1 = os.path.basename(video_file)



        saving_frames_per_second = min(video_clip.fps, SAVING_FRAMES_PER_SECOND)
        step = 1 / video_clip.fps if saving_frames_per_second == 0 else 1 / saving_frames_per_second

        self.total_frames = len(np.arange(0, video_clip.duration, step))

        processed_frames = 0

        for current_duration in np.arange(0, video_clip.duration, step):
            frame_duration_formatted = self.format_timedelta(timedelta(seconds=current_duration)).replace(":", "-")
            frame_filename = os.path.join(output_folder, f"frame_{video_file_1}_{frame_duration_formatted}.jpg")
            video_clip.save_frame(frame_filename, current_duration)
            processed_frames += 1
            if processed_frames == self.total_frames:
                self.on_exit()

    def select_video_file(self):
        video_file = fd.askopenfilename(title="Select a Video File")
        return video_file

    def select_output_folder(self):
        output_folder = fd.askdirectory(title="Select Output Folder")
        return output_folder

    def process_video(self):
        video_file = self.select_video_file()
        if video_file:
            output_folder = self.select_output_folder()
            if output_folder:
                self.extract_frames(video_file, output_folder)

    def on_exit(self):
        root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    frame_parser = FrameParser(root)
    root.mainloop()

