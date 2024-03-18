import cv2 as cv
import os
from ultralytics import YOLO
import pyttsx3
import threading
import queue

class Model:
    def __init__(self):
        self.path = os.path.abspath("2.MOV")
        self.model = YOLO("yolov8n_custom_9.pt")
        self.engine = pyttsx3.init()
        self.voice_queue = queue.Queue()

        # Start voice output thread
        voice_thread = threading.Thread(target=self.voice_output_thread)
        voice_thread.daemon = True
        voice_thread.start()

    def open_video(self):
        # Open the video file
        video_path = self.path
        cap = cv.VideoCapture(video_path)
        return cap

    def voice_output(self, text):
        self.voice_queue.put(text)

    def voice_output_thread(self):
        while True:
            text = self.voice_queue.get()
            self.engine.say(text)
            self.engine.runAndWait()
            self.voice_queue.task_done()

    def video_processing(self):
        open_video = self.open_video()
        # Loop through the video frames
        while open_video.isOpened():
            # Read a frame from the video
            success, frame = open_video.read()

            if success:
                # Run YOLOv8 inference on the frame
                results = self.model(frame)
                clss = results[0].boxes.cls.cpu().tolist()

                # Visualize the results on the frame
                annotated_frame = results[0].plot()
                if clss != []:
                    for i in clss:
                        sign = results[0].names.get(int(i))
                        if sign == "give_way":
                            self.voice_output("Внимание впереди знак уступи дорогу")
                        elif sign != "give_way":
                            break

                # Display the annotated frame
                cv.imshow("YOLOv8 Inference", annotated_frame)
                if cv.waitKey(1) & 0xFF == ord("q"):
                    break

            else:
                # Break the loop if the end of the video is reached
                break

        # Release the video capture object and close the display window
        open_video.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    model = Model()
    model.video_processing()