import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

capture = cv2.VideoCapture(0)
width, height = capture.get(cv2.CAP_PROP_FRAME_WIDTH), capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

mp_drawing, mp_drawing_styles, mp_pose = mp.solutions.drawing_utils, mp.solutions.drawing_styles, mp.solutions.pose

MODEL_PATH = 'model/efficientdet_lite0.tflite'

USER_PATH = "user.png"
# USER_PATH = 'static/frames/user.png'

options = vision.ObjectDetectorOptions(

  base_options = python.BaseOptions(model_asset_path = MODEL_PATH),
  score_threshold = 0.5,
  max_results = 1

)

detector = vision.ObjectDetector.create_from_options(options)

def coordinates(cropprocessed):

    lshoulder = cropprocessed.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    lshoulderx, lshouldery = lshoulder.x * width, lshoulder.y * height

    rshoulder = cropprocessed.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    rshoulderx, rshouldery = rshoulder.x * width, rshoulder.y * height

    lelbow = cropprocessed.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
    lelbowx, lelbowy = lelbow.x * width, lelbow.y * height

    relbow = cropprocessed.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
    relbowx, relbowy = relbow.x * width, relbow.y * height

    lwrist = cropprocessed.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
    lwristx, lwristy = lwrist.x * width, lwrist.y * height

    rwrist = cropprocessed.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
    rwristx, rwristy = rwrist.x * width, rwrist.y * height

    rhip = cropprocessed.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
    rhipx, rhipy = rhip.x * width, rhip.y * height

    lhip = cropprocessed.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
    lhipx, lhipy = lhip.x * width, lhip.y * height

    rknee = cropprocessed.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
    rkneex, rkneey = rknee.x * width, rknee.y * height

    lknee = cropprocessed.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
    lkneex, lkneey = lknee.x * width, lknee.y * height

    rankle = cropprocessed.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]
    ranklex, rankley = rankle.x * width, rankle.y * height

    lankle = cropprocessed.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
    lanklex, lankley = lankle.x * width, lankle.y * height

    return lshoulderx, lshouldery, rshoulderx, rshouldery, lelbowx, lelbowy, relbowx, relbowy, lwristx, lwristy, rwristx, rwristy, rhipx, rhipy, lhipx, lhipy, rkneex, rkneey, lkneex, lkneey, ranklex, rankley, lanklex, lankley

with mp_pose.Pose(min_detection_confidence = 0.8, min_tracking_confidence = 0.8) as pose:

    log = open("log.txt", "w")

    while capture.isOpened():

        read, canvas = capture.read()

        if not read:

            print("Dropped a Frame")
            continue

        cv2.imwrite("temp.png", canvas)
        image = mp.Image.create_from_file("temp.png")
        save = np.copy(image.numpy_view())

        for detection in detector.detect(image).detections:

            bound = detection.bounding_box

            start = bound.origin_x, bound.origin_y
            end = bound.origin_x + bound.width, bound.origin_y + bound.height

        crop = save[start[1] : end[1], start[0] : end[0]]

        canvas.flags.writeable = False  # Temporarily mark the image as not writeable to improve performance when passing to mediapipe

        canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
        rawprocessed = pose.process(canvas)
        cv2.imwrite(USER_PATH, canvas)

        cropprocessed = pose.process(crop)

        canvas.flags.writeable = True

        canvas = cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR)
        crop = cv2.cvtColor(crop, cv2.COLOR_RGB2BGR)

        if cropprocessed.pose_landmarks:

            mp_drawing.draw_landmarks(

                crop,
                cropprocessed.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()

            )

            log.write(f"{coordinates(cropprocessed)[1:-1]}\n")

        else:

            log.write("None, " * 23 + "None\n")

        cv2.imshow("EchoPose", cv2.flip(crop, 1))  # Flip video

        if cv2.waitKey(5) & 0xFF in (27, 81, 113):

            break

capture.release()