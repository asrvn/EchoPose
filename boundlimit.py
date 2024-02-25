import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

BOXCOLOR = (0, 0, 0)
IMAGE_FILE = 'image.jpg'
MODEL_PATH = 'model/efficientdet_lite0.tflite'

options = vision.ObjectDetectorOptions(

  base_options = python.BaseOptions(model_asset_path = MODEL_PATH),
  score_threshold = 0.5,
  max_results = 1

)
detector = vision.ObjectDetector.create_from_options(options)

image = mp.Image.create_from_file(IMAGE_FILE)

detection_result = detector.detect(image)

annotate = np.copy(image.numpy_view())

for detection in detection_result.detections:

  bbox = detection.bounding_box

  start_point = bbox.origin_x, bbox.origin_y
  end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height

  cv2.rectangle(annotate, start_point, end_point, BOXCOLOR, 1)

annotateRGB = cv2.cvtColor(annotate, cv2.COLOR_BGR2RGB)
cv2.imshow('MediaPipe Object Detection', annotateRGB)
cv2.waitKey(0)
