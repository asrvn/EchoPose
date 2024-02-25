import os
import cv2
import yt_dlp
from yt_dlp.utils import download_range_func

# Units: seconds
start = 2  # start time arg
end = 7  # end time arg

source = "/Users/anikethluchmapurkar/Downloads/vid.webm"  # this is the arg

currDir = "/Users/anikethluchmapurkar/Desktop/hackathons/2024-hacktj/EchoPose"  # change this for real comp

outputFileName = "vid" #change this to whatever
placeToSave = currDir
    

if "?" in source:
    
    yt_opts = {
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

