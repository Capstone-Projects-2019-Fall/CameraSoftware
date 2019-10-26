import datetime as dt
from email.mime.image import MIMEImage
import os
import firebase_admin
from firebase import firebase
from firebase_admin import credentials
from firebase_admin import storage
from google.cloud import firestore
from firebase_admin import firestore

cred=credentials.Certificate('/home/pi/Desktop/CameraSoftware/cred.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'mspi-a4b75.appspot.com'
})
storage_client = firestore.client()
bucket = storage.bucket()


def upload():
    print("Sending Image to Firestore...")
    blob = bucket.blob( 'images/'+str(dt.datetime.now()) + '.jpg')
    outfile='/home/pi/Desktop/CameraSoftware/WhoDat.jpg'
    blob.upload_from_filename(outfile)
    print("Image was uploaded to firestore!")
    fireapp = firebase.FirebaseApplication('https://mspi-a4b75.firebaseio.com',  None)
    result = fireapp.post('/signal', {'signal':'Charrrrrlie'})
    print('DB has been signaled...')
