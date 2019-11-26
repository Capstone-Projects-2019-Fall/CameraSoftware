import pyrebase
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from firebase_admin import firestore


config = {
    "apiKey": "AIzaSyC2AMehEW9xsxtLdVKHzZG7ENNh2wrBNw0",
    "authDomain": "mspi-a4b75.firebaseapp.com",
    "databaseURL": "https://mspi-a4b75.firebaseio.com",
    "storageBucket": "mspi-a4b75.appspot.com",   
    }
cred=credentials.Certificate('/home/pi/Desktop/CameraSoftware/cred.json')
    #cred=credentials.Certificate('cred.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'mspi-a4b75.appspot.com'
})

storage_client = firestore.client()
firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()

test123 = db.child("webrtctest").order_by_child("sender").equal_to("Pi1").get()

print(test123)