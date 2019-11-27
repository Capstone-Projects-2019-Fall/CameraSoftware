import datetime as dt
import firebase_admin
from firebase import firebase
from firebase_admin import credentials
from firebase_admin import storage
from google.cloud import firestore
from firebase_admin import firestore
import settings


def upload():
    #initialize files
    outfile = None
    blob = None
    bucket = storage.bucket()
    
    #Name file by current time
    name = str(dt.datetime.now())
    
    #Picture to be sent to Firebase
    outfile='/home/pi/Desktop/CameraSoftware/WhoDat.jpg'
    print("Sending Image to Firestore...")
    #Upload image blob
    blob = bucket.blob( settings.userID + '/images/'+ name + '.jpg')
    blob.upload_from_filename(outfile)
    print("Image was uploaded to firestore!")
    
    #Video to be Sent to Firebase
    outfile='/home/pi/Desktop/CameraSoftware/video.mp4'
    print("Sending Video to Firestore...")
    #Upload video blob
    blob = bucket.blob(settings.userID +'/videos/'+ name + '.mp4')
    blob.upload_from_filename(outfile)
    print("Video was uploaded to firestore!")

    #Signal Database
    fireapp = firebase.FirebaseApplication('https://mspi-a4b75.firebaseio.com',  None)
    fireapp.post('/signal', {'signal':'Charrrrrlie'})
    print('DB has been signaled...')
