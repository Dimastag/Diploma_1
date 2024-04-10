import os
import cv2
from threading import Thread, Lock
import pyttsx3
from ultralytics import YOLO


class RecordMode:
    def __init__(self):
        self.path = os.path.abspath("2.MOV")
        self.model = YOLO("yolov8n_custom_9.pt")
        self.engine = pyttsx3.init()
        self.crosswalk_detected = False
        self.lock = Lock()  # Создание объекта мьютекса

    def voice_output(self, txt):
        """
        :param txt: Параметр отвечающий за текст речевого помошника
        :return:
        """
        self.engine.say(txt)
        self.engine.runAndWait()

    def exit_condition(self, key):
        return key == ord('q')

    def real_time(self):
        """
        Функция обрабатывающая видео в реальном времени с помощью библиотеки OpenCV и
        нейросети YOLOv8
        """
        video_capture = cv2.VideoCapture(0)

        while video_capture.isOpened():
            # Чтение кадров с видео
            success, frame = video_capture.read()

            if success:
                # Запуск YOLOv8 по фреймам
                results = self.model.predict(frame)

                # Здесь получаем название классов из модели
                clss = results[0].boxes.cls.cpu().tolist()

                annotated_frame = results[0].plot()

                # Цикл где происходит срабатывание речевого помошника в зависимости от появившегося класса на экране
                if clss != []:
                    for i in clss:
                        sign = results[0].names.get(int(i))
                        if sign == "give_way":
                            with self.lock:
                                Thread(target=self.voice_output, args=("Внимание уступи дорогу",)).start()
                        if sign == "crosswalk_2":
                            with self.lock:
                                Thread(target=self.voice_output, args=("Внимание пешеходный переход",)).start()

                # Отображение в каждом кадре названий найденных объектов
                cv2.imshow("YOLOv8 Inference", annotated_frame)
                key = cv2.waitKey(1)
                if self.exit_condition(key):
                    break

        # Отпускает видеозахват и зыкрывает окно
        video_capture.release()
        cv2.destroyAllWindows()

    def record_mode(self):
        """
        Функция обрабатывающая видео в режиме записи с помощью библиотеки OpenCV и
        нейросети YOLOv8
        """
        cap = cv2.VideoCapture(self.path)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            results = self.model(frame)

            # Здесь получаем название классов из модели
            clss = results[0].boxes.cls.cpu().tolist()

            # Визуализация названий в каждом кадре
            annotated_frame = results[0].plot()
            if clss != []:
                for i in clss:
                    sign = results[0].names.get(int(i))
                    if sign == "give_way":
                        with self.lock:
                            Thread(target=self.voice_output, args=("Внимание уступи дорогу",)).start()
                    if sign == "crosswalk_2":
                        with self.lock:
                            Thread(target=self.voice_output, args=("Внимание пешеходный переход",)).start()

            cv2.imshow("Video", annotated_frame)
            key = cv2.waitKey(1)
            if self.exit_condition(key):
                break

        cap.release()
        cv2.destroyAllWindows()
