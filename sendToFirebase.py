import datetime as dt
import firebase_admin
from firebase import firebase
from firebase_admin import credentials
from firebase_admin import storage
from google.cloud import firestore
from firebase_admin import firestore
import settings


def upload():
    outfile = None
    blob = None
    bucket = storage.bucket()
    
    name = str(dt.datetime.now())
    
    #Upload image
    outfile='/home/pi/Desktop/CameraSoftware/WhoDat.jpg'
    #outfile='WhoDat.jpg'
    print("Sending Image to Firestore...")
    blob = bucket.blob( settings.userID + '/images/'+ name + '.jpg')
    blob.upload_from_filename(outfile)
    print("Image was uploaded to firestore!")
    
    #Upload Video
    outfile='/home/pi/Desktop/CameraSoftware/video.mp4'
    #outfile='video.mp4'
    print("Sending Video to Firestore...")
    blob = bucket.blob(settings.userID +'/videos/'+ name + '.mp4')
    blob.upload_from_filename(outfile)
    print("Video was uploaded to firestore!")


    fireapp = firebase.FirebaseApplication('https://mspi-a4b75.firebaseio.com',  None)
    fireapp.post('/signal', {'signal':'Charrrrrlie'})
    print('DB has been signaled...')
