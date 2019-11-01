# import the necessary packages
from libs.pyimagesearch.motion_detection import SingleMotionDetector
from imutils.video import VideoStream
from sendToFirebase import upload
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
import imutils
import time
import cv2
from ttictoc import TicToc
import numpy as np
import os
import sys

filename = 'video.mp4'
frames_per_second = 24.0
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

# grab resolution dimensions and set video capture to it.


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
    # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}


def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['mp4']


# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful for multiple browsers/tabs
# are viewing tthe stream)
outputFrame = None
lock = threading.Lock()
isRecording = False
# initialize a flask object
app = Flask(__name__)


# initialize the video stream and allow the camera sensor to
# warmup
#vs = VideoStream(usePiCamera=1).start()
vs = VideoStream(src=0).start()
time.sleep(2.0)
timer = TicToc()


def detect_motion(frameCount):
        # grab global references to the video stream, output frame, and
        # lock variables
    global vs, outputFrame, lock

    # initialize the motion detector and the total number of frames
    # read thus far
    md = SingleMotionDetector(accumWeight=0.1)
    total = 0
    isRecording = False

    # Starts recording
    cap = cv2.VideoCapture(0)
    out = cv2.VideoWriter(filename, get_video_type(
        filename), 25, get_dims(cap, res))

    # Starts Timer
    timer.tic()

    t = threading.currentThread()
    # loop over frames from the video stream
    while getattr(t, "do_run", True):

        # record Video
        ret, frame = cap.read()
        out.write(frame)

        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        frame = vs.read()
        frame = imutils.resize(frame, width=400)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # grab the current timestamp and draw it on the frame
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        # if the total number of frames has reached a sufficient
        # number to construct a reasonable background model, then
        # continue to process the frame
        if total > frameCount:
            # detect motion in the image
            motion = md.detect(gray)
            if(timer.toc() is not None):
                # print(timer.toc())
                if(motion is None and timer.toc() >= 5):
                    cap.release()
                    out.release()

                    cv2.destroyAllWindows()
                    print("video Ends")
                    upload("video")

                    t.do_run = False

            # cehck to see if motion was found in the frame
            if motion is not None:
                timer.tic()
                if isRecording == False:
                    print("Video Starts Here")
                    isRecording = True

                # unpack the tuple and draw the box surrounding the
                # "motion area" on the output frame
                (thresh, (minX, minY, maxX, maxY)) = motion
                cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                              (0, 0, 255), 2)

        # update the background model and increment the total number
        # of frames read thus far
        md.update(gray)
        total += 1

        # acquire the lock, set the output frame, and release the
        # lock
        with lock:
            outputFrame = frame.copy()


# check to see if this is the main thread of execution
if __name__ == '__main__':
  # start a thread that will perform motion detection
    # t = threading.Thread(target=detect_motion, args=(
    #     32,))
    # t.daemon = True
    # t.start()
    # t.join()
    # sys.exit()

    # # start the flask app
    # app.run(debug=True,threaded=True, use_reloader=False)

# release the video stream pointer
    vs.stop()
