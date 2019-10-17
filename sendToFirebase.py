import json
import datetime as dt
from email.mime.image import MIMEImage
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from google.cloud import firestore
from firebase_admin import firestore

cred=credentials.Certificate('/home/pi/ObjectDetectionRaspPi/cred.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'mspi-a4b75.appspot.com'
})
storage_client = firestore.client()
bucket = storage.bucket()


def upload():
	print("Sending Image to Firestore...")
	blob = bucket.blob( str(dt.datetime.now()) + '.jpg')
	outfile='/home/pi/ObjectDetectionRaspPi/WhoDat.jpg'
	blob.upload_from_filename(outfile)
	print("Image was uploaded to firestore!")
