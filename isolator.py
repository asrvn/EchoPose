import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

IMAGE_FILE = 'walking.jpg'
MODEL_PATH = 'model/efficientdet_lite0.tflite'

options = vision.ObjectDetectorOptions(

  base_options = python.BaseOptions(model_asset_path = MODEL_PATH),
  score_threshold = 0.5,
  max_results = 1

)

detector = vision.ObjectDetector.create_from_options(options)

image = mp.Image.create_from_file(IMAGE_FILE)
save = np.copy(image.numpy_view())

for detection in detector.detect(image).detections:

  bound = detection.bounding_box

  start = bound.origin_x, bound.origin_y
  end = bound.origin_x + bound.width, bound.origin_y + bound.height

crop = save[start[1] : end[1], start[0] : end[0]]
crop = cv2.cvtColor(crop, cv2.COLOR_RGB2BGR)

cv2.imshow('MediaPipe Object Detection', crop)
cv2.waitKey(0)