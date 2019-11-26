import pyrebase
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from firebase_admin import firestore
import settings

def download_faces():
    config = {
        "apiKey": "AIzaSyC2AMehEW9xsxtLdVKHzZG7ENNh2wrBNw0",
        "authDomain": "mspi-a4b75.firebaseapp.com",
        "databaseURL": "https://mspi-a4b75.firebaseio.com",
        "storageBucket": "mspi-a4b75.appspot.com",   
        }

    storage_client = firestore.client()
    firebase = pyrebase.initialize_app(config)

    storage = firebase.storage()

    user_collection = storage_client.collection('users')
    results = user_collection.document(settings.userID).get()

    faces = results.to_dict().get('familiarFaces')

    for face in faces:
        storage.child(settings.userID+"/Training/"+face).download("/home/pi/Desktop/CameraSoftware/familiarFaces/"+face)
