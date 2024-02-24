import cv2
import mediapipe as mp

capture = cv2.VideoCapture(0)
width, height = capture.get(cv2.CAP_PROP_FRAME_WIDTH), capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

mp_drawing, mp_drawing_styles, mp_pose = mp.solutions.drawing_utils, mp.solutions.drawing_styles, mp.solutions.pose

def remap(value):

    return 1 - value

with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:

    while capture.isOpened():

        read, img = capture.read()
        
        if not read:

            print("Dropped a Frame")
            continue

        # Temporarily mark the image as not writeable to improve performance when passing to mediapipe

        img.flags.writeable = False

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        processed = pose.process(img)

        img.flags.writeable = True

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if processed.pose_landmarks:

            mp_drawing.draw_landmarks(

                img,
                processed.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec = mp_drawing_styles.get_default_pose_landmarks_style()

            )

            x = remap(processed.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x) * width
            y = remap(processed.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y) * height
            print(f"Nose: ({x}, {y})")

        cv2.imshow("pose", cv2.flip(img, 1)) #flip video

        if cv2.waitKey(5) & 0xFF == 27:

            break

capture.release()