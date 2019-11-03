import os
import webbrowser

#starts webRTC
webbrowser.open('file://' + os.path.realpath("firebaseRTC_client2.html"))
exec(open("/home/pi/Desktop/CameraSoftware/object_detection.py").read())
