import os
import webbrowser
import time
#starts webRTC
#webbrowser.open('file://' + os.path.realpath("firebaseRTC_client2.html"))
while True:
    time.sleep(1)
    exec(open("/home/pi/Desktop/CameraSoftware/object_detection.py").read())
