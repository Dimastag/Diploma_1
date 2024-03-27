import cv2 as cv
import os
from ultralytics import YOLO
import pyttsx3
import threading
import queue

class RecordMode:
    def __init__(self):
        self.path = os.path.abspath("2.MOV")
        self.model = YOLO("yolov8n_custom_9.pt")
        self.engine = pyttsx3.init()
        self.signs_queue = queue.Queue()
        self.crosswalk_detected = False

        signs_thread = threading.Thread(target=self.process_signs)
        signs_thread.daemon = True
        signs_thread.start()

    def open_video(self):
        # Open the video file
        video_path = self.path
        cap = cv.VideoCapture(video_path)
        return cap

    def process_signs(self):
        while  True:
            sign_text = self.signs_queue.get()
            self.voice_output(sign_text)
            self.signs_queue.task_done()
            # if self.crosswalk_detected == False:
            #         self.signs_queue.task_done()

    def voice_output(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.endLoop()
    def real_time(self):
        # real_time = self.model.predict(source=0)
        video_capture = cv.VideoCapture(0)

        while video_capture.isOpened():
            # Read a frame from the video
            success, frame = video_capture.read()

            if success:
                # Запуск YOLOv8 по фреймам
                results = self.model.predict(frame)

                # Здесь получаем название классов из модели
                clss = results[0].boxes.cls.cpu().tolist()

                # Визуализация названий в каждом кадре
                annotated_frame = results[0].plot()

                if clss != []:
                    for i in clss:
                        sign = results[0].names.get(int(i))
                        print(self.crosswalk_detected)
                        if sign == "crosswalk_2":
                            self.signs_queue.put("Внимание впереди пешеходный переход")
                        if sign == "No_parking":
                            self.signs_queue.put("Внимание парковка запрещена")
                        if sign == "give_way":
                            self.signs_queue.put("Внимание уступи дорогу")

                # Отображение в каждом кадре названий найденных объектов
                cv.imshow("YOLOv8 Inference", annotated_frame)
                if cv.waitKey(1) & 0xFF == ord("q"):
                    break

            else:
                # Break the loop if the end of the video is reached
                break

        # Release the video capture object and close the display window
        video_capture.release()
        cv.destroyAllWindows()

    def video_processing(self):
        ''' С помощью библиотеки opencv делим видео на кадры '''
        open_video = self.open_video()
        # Loop through the video frames
        while open_video.isOpened():
            # Read a frame from the video
            success, frame = open_video.read()

            if success:
                # Запуск YOLOv8 по фреймам
                results = self.model(frame)

                # Здесь получаем название классов из модели
                clss = results[0].boxes.cls.cpu().tolist()

                # Визуализация названий в каждом кадре
                annotated_frame = results[0].plot()

                if clss != []:
                    for i in clss:
                        sign = results[0].names.get(int(i))
                        print(self.crosswalk_detected)
                        if sign == "crosswalk_2":
                            self.signs_queue.put("Внимание впереди пешеходный переход")
                        if sign == "No_parking":
                            self.signs_queue.put("Внимание парковка запрещена")
                        if sign == "give_way":
                            self.signs_queue.put("Внимание уступи дорогу")

                # Отображение в каждом кадре названий найденных объектов
                cv.imshow("YOLOv8 Inference", annotated_frame)
                if cv.waitKey(1) & 0xFF == ord("q"):
                    break

            else:
                # Break the loop if the end of the video is reached
                break

        # Release the video capture object and close the display window
        open_video.release()
        cv.destroyAllWindows()