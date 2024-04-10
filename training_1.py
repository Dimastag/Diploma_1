from ultralytics import YOLO


model = YOLO("yolov8n_custom_8.pt")  # Модель YOLOv8n

results = model.train(
                         data='data.yaml',
                         imgsz=640,
                         epochs=100,
                         batch=-1,
                         name='yolov8n_custom_9'
                                )