from ultralytics import YOLO


model = YOLO("yolo8n_custom_11.pt")  # Модель YOLOv8n

results = model.train(
                         data='data.yaml',
                         imgsz=640,
                         epochs=200,
                         batch=8,
                         name='yolov8n_custom_12'
                                )