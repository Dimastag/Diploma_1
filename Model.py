import cv2 as cv
import sys
import os
from ultralytics import YOLO
import pyttsx3


class Model:


    def  __init__(self):
        self.path = os.path.abspath("C:\\Users\\Dmitrii\\PycharmProjects\\Diploma_1\\interface_data\\2.MOV")
        self.model = YOLO("yolov8n_custom_9.pt")


    def open_video(self):
    # Open the video file
        video_path = self.path
        cap = cv.VideoCapture(video_path)
        return cap

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
                        with open("log.txt", "a+") as f:
                                f.write(sign + " , ")
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

    # def sound_notification(self):
    #     engine = pyttsx3.init()
    #     engine.say("Привет, мир!")
    #     engine.runAndWait()

if __name__=="__main__":
    model = Model()
    model.video_processing()