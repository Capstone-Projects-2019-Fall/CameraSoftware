import datetime as dt
from email.mime.image import MIMEImage
import os
import firebase_admin
from firebase import firebase
from firebase_admin import credentials
from firebase_admin import storage
from google.cloud import firestore
from firebase_admin import firestore

#Get Credentials from JSON
cred=credentials.Certificate('/home/pi/Desktop/CameraSoftware/cred.json')
#cred=credentials.Certificate('cred.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'mspi-a4b75.appspot.com'
})
storage_client = firestore.client()
bucket = storage.bucket()


def upload():
    outfile = None
    blob = None
    
    name = str(dt.datetime.now())
    
    #Upload image
    outfile='/home/pi/Desktop/CameraSoftware/WhoDat.jpg'
    #outfile='WhoDat.jpg'
    print("Sending Image to Firestore...")
    blob = bucket.blob( 'images/'+ name + '.jpg')
    blob.upload_from_filename(outfile)
    print("Image was uploaded to firestore!")
    
    #Upload Video
    outfile='/home/pi/Desktop/CameraSoftware/video.h264'
    #outfile='video.mp4'
    print("Sending Video to Firestore...")
    blob = bucket.blob( 'videos/'+ name + '.mp4')
    blob.upload_from_filename(outfile)
    print("Video was uploaded to firestore!")


    fireapp = firebase.FirebaseApplication('https://mspi-a4b75.firebaseio.com',  None)
    fireapp.post('/signal', {'signal':'Charrrrrlie'})
    print('DB has been signaled...')
