import cv2
import mediapipe as mp

capture = cv2.VideoCapture(0)
width, height = capture.get(cv2.CAP_PROP_FRAME_WIDTH), capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

mp_drawing, mp_drawing_styles, mp_pose = mp.solutions.drawing_utils, mp.solutions.drawing_styles, mp.solutions.pose

def coordinates(processed):

    lshoulder = processed.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
    lshoulderx, lshouldery = lshoulder.x * width, lshoulder.y * height

    rshoulder = processed.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
    rshoulderx, rshouldery = rshoulder.x * width, rshoulder.y * height

    lelbow = processed.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
    lelbowx, lelbowy = lelbow.x * width, lelbow.y * height

    relbow = processed.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
    relbowx, relbowy = relbow.x * width, relbow.y * height

    lwrist = processed.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
    lwristx, lwristy = lwrist.x * width, lwrist.y * height

    rwrist = processed.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
    rwristx, rwristy = rwrist.x * width, rwrist.y * height

    rhip = processed.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
    rhipx, rhipy = rhip.x * width, rhip.y * height

    lhip = processed.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
    lhipx, lhipy = lhip.x * width, lhip.y * height

    rknee = processed.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
    rkneex, rkneey = rknee.x * width, rknee.y * height

    lknee = processed.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
    lkneex, lkneey = lknee.x * width, lknee.y * height

    rankle = processed.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]
    ranklex, rankley = rankle.x * width, rankle.y * height

    lankle = processed.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]
    lanklex, lankley = lankle.x * width, lankle.y * height

    return lshoulderx, lshouldery, rshoulderx, rshouldery, lelbowx, lelbowy, relbowx, relbowy, lwristx, lwristy, rwristx, rwristy, rhipx, rhipy, lhipx, lhipy, rkneex, rkneey, lkneex, lkneey, ranklex, rankley, lanklex, lankley

with mp_pose.Pose(min_detection_confidence = 0.8, min_tracking_confidence = 0.8) as pose:

    log = open("log.txt", "w")

    while capture.isOpened():

        read, canvas = capture.read()
        
        if not read:

            print("Dropped a Frame")
            continue

        # Temporarily mark the image as not writeable to improve performance when passing to mediapipe

        canvas.flags.writeable = False

        canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
        processed = pose.process(canvas)

        canvas.flags.writeable = True

        canvas = cv2.cvtColor(canvas, cv2.COLOR_RGB2BGR)

        if processed.pose_landmarks:

            mp_drawing.draw_landmarks(

                canvas,
                processed.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec = mp_drawing_styles.get_default_pose_landmarks_style()

            )

            log.write(str(coordinates(processed))[1:-1] + "\n")

        else:

            log.write("None, " * 23 + "None\n")

        cv2.imshow("EchoPose", cv2.flp(canvas, 1)) # Flip video

        if cv2.waitKey(5) & 0xFF in (27, 81, 113):

            break

capture.release()