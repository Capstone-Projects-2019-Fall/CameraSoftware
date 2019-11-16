# import the necessary packages

from sendToFirebase import upload
from libs.pyimagesearch.motion_detection import SingleMotionDetector
import threading
import imutils
import cv2
from ttictoc import TicToc
import numpy as np
import os
import settings

filename = 'video.mp4'
frames_per_second = 30.0
res = '720p'

def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)


# Standard Video Dimensions Sizes
STD_DIMENSIONS = {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

# grab resolution dimensions and set video capture to it
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width, height = STD_DIMENSIONS[res]
    # change the current caputre device
    # to the resulting resolution
    change_res(cap, width, height)
    return width, height


# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    'mp4': cv2.VideoWriter_fourcc(*'H264'),
    #'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}


def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['mp4']


# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)


def detect_motion(frameCount):
        # grab global references to the video stream, output frame, and
        # lock variables
    global outputFrame, lock
    
    outputFrame = None
    #lock = threading.Lock()
    timer = TicToc()
    

    # initialize the motion detector and the total number of frames
    # read thus far
    md = SingleMotionDetector(accumWeight=0.2)
    total = 0
    record = True

    # Starts recording
    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(filename, get_video_type(
        filename), 25, get_dims(cap, res))
    
    
    

    # Starts Timer
    timer.tic()
    #Grab reference to current thread
    #t = threading.currentThread()
    # loop over frames from the video stream
    
    #While Thread is not told to stop, keep running
    #while getattr(t, "do_run", True):
    while (record == True):

        # Read video streaming frames and send it to video
        ret, frame = cap.read()
        out.write(frame)

        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        

        # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame
        if total > 32:
            # detect motion in the image
            motion = md.detect(gray)
            if(motion is not None):
               print("motion")
               timer.tic()
            if(timer.toc() is not None):
                # print(timer.toc())
                if((motion is None and timer.toc() >= 10) or settings.lock == True):
                    #Stops recording + Cleanup
                    cap.release()
                    out.release()
                    out=None
                    cap=None
                    md= None
                    total = 0
                    cv2.destroyAllWindows()
                    print("video Ends")
                    record = False
                    threading.Thread(target=upload).start()
                    #Tells thread to stop
                    #t.do_run = False
                    break

        # update the background model and increment the total number
        # of frames read thus far
        md.update(gray)
        total += 1

        # acquire the lock, set the output frame, and release the
        # lock
        #with lock:
        outputFrame = frame.copy()




