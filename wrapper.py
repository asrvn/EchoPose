import cv2
import mediapipe as mp
import os
import yt_dlp
from yt_dlp.utils import download_range_func

# have to add trimming
def app(outfileName):  # void - performs pose tracking and logs to file for a certain dancer (pro or user)
    capture = cv2.VideoCapture(outfileName+".mp4") 
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

        log = open(outfileName+"Logs.txt", "w")  # outfileName = user or pro

        while capture.isOpened():

            read, canvas = capture.read()
            
            if not read:

                print("Dropped a Frame")
                break

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

            
            if cv2.waitKey(5) & 0xFF in (27, 81, 113):

                break

    capture.release()
    
def comparison():  # returns flagged frames 
    with open("profLogs.txt", "r") as profData: 

        profCoords = [line.split(", ") for line in profData.readlines()]

    with open("userLogs.txt", "r") as userData: 

        userCoords = [line.split(", ") for line in userData.readlines()]

    threshold = 500 # test it

    flagged = []

    for frame in range(len(profCoords)):

        for part in range(24):

            if profCoords[frame][part] and not userCoords[frame][part]:

                flagged.append((frame, part, None)) # feedback is third arg

            if (dist := abs(float(profCoords[frame][part]) - float(userCoords[frame][part]))) >= threshold:

                flagged.append((frame, part, dist)) # feedback is third arg
                
    return flagged
                
def filehandler(source, start, end, outfileName):  # void - performs file downloads
    # Units: seconds
    #start = 2  # start time arg
    #end = 7  # end time arg

    #source = "/Users/anikethluchmapurkar/Downloads/vid.webm"  # this is the arg

    
    currDir = "/Users/anikethluchmapurkar/Desktop/hackathons/2024-hacktj/EchoPose"  # change this for real comp

    outputFileName = outfileName #outfileName = user or pro
    placeToSave = currDir
    file_format="mp4"

    if "?" in source:
        
        yt_opts = {
            'format': f'bestvideo[ext={file_format}]+bestaudio[ext={file_format}]/best[ext={file_format}]',
            'verbose': False,
            'download_ranges': download_range_func(None, [(start, end)]),
            'outtmpl': os.path.join(placeToSave, outputFileName),
            'force_keyframes_at_cuts': False  # Test without it
        }

        with yt_dlp.YoutubeDL(yt_opts) as ydl:

            ydl.download(source)

    else:
        
        full_destination_path = os.path.join(placeToSave, outputFileName + ".mp4")

        # trimming
        cap = cv2.VideoCapture(source)

        fps = cap.get(cv2.CAP_PROP_FPS)
        totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        startFrame = int(start * fps)
        endFrame = min(int(end * fps), totalFrames - 1)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
        out = cv2.VideoWriter(full_destination_path, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

        # Read and write frames within the specified range
        for _ in range(startFrame, endFrame + 1):
            
            ret, frame = cap.read()
            
            if not ret: break

            out.write(frame)

        # Release the video capture and writer objects
        cap.release()
        out.release()
