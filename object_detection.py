# import the necessary packages
from imutils.video import VideoStream
import numpy as np
from mail import sendEmail
from facerecognition import recognize_faces
import imutils
import cv2
import threading
import settings

def detect_object():
    # initialize the list of class labels MobileNet SSD was trained to
    # detect, then generate a set of bounding box colors for each class
    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
        "sofa", "train", "tvmonitor"]
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    #Set holds only what we want to detect
    DETECT = set(["person"])

    # load our serialized model from disk
    print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

    # initialize the video stream
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()

    #Flag to break loop
    flag = True
    
    # loop over the frames from the video stream
    while ((flag is True) and (settings.lock is False) and (settings.active is True)):
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 800 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=800)

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
            0.007843, (300, 300), 127.5)

        # pass the blob through the network and obtain the detections and
        # predictions
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence > 0.5:
                # extract the index of the class label from the
                # `detections`, then compute the (x, y)-coordinates of
                # the bounding box for the object
                idx = int(detections[0, 0, i, 1])
                if CLASSES[idx] not in  DETECT:
                    continue
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # draw the prediction on the frame
                label = "{}: {:.2f}%".format(CLASSES[idx],
                    confidence * 100)
                cv2.rectangle(frame, (startX, startY), (endX, endY),
                    COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                
                # show the output frame
                #cv2.imshow("Frame", frame)
                key = cv2.waitKey(1) & 0xFF
                cv2.imwrite('/home/pi/Desktop/CameraSoftware/WhoDat.jpg',frame)
                #cv2.imwrite('/Users/nick/Desktop/cameraRepo/CameraSoftware/WhoDat.jpg',frame)
                
                print("Recognizing Faces...")
                people = list()
                people = recognize_faces()
                
                print("Sending email...")
                threading.Thread(target=sendEmail, args=[people]).start()
                print("done!")
                
                vs.stop()
                
                #breaks from whil loop
                flag = False

                # do a bit of cleanup
                cv2.destroyAllWindows()
                break
                
            
    #Release camera
    vs.stream.release()


