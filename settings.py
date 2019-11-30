#--------------------------------------------------------------------------------------------------#
#Imports

import os
import face_recognition
import firebase_admin
from firebase import firebase
from firebase_admin import credentials
from firebase_admin import storage
from google.cloud import firestore
from firebase_admin import firestore
from downloadFaces import download_faces


def init():
#Initializer
#--------------------------------------------------------------------------------------------------#    
#Starting FireStore
    cred=credentials.Certificate('/home/pi/Desktop/CameraSoftware/cred.json')
    #cred=credentials.Certificate('cred.json')
    app = firebase_admin.initialize_app(cred, {
        'storageBucket': 'mspi-a4b75.appspot.com'
    })
    storage_client = firestore.client()
    
#--------------------------------------------------------------------------------------------------#  
#Globals
    global lock
    global unlock
    global cameraID
    global known_face_encodings
    global known_face_names
    global userID
    global active
    global ready
#--------------------------------------------------------------------------------------------------#      
#Set Globals  
    cameraID = "00123"
    lock = False
    unlock = True
    known_face_encodings = []
    
#Get UserID
    user_collection = storage_client.collection('users')
    results = user_collection.where('cameraIds', u'array_contains', cameraID).get()
    for item in results:
        userID = item.id
    
#Download Faces to Be Recognized
    download_faces()
    #print("Faces Downloaded!")

#Clear WebRTC
    web_rtc_col = storage_client.collection('webrtctest')
    to_be_deleted = web_rtc_col.where(u'sender', u'==', cameraID).get()
    lala = firebase.FirebaseApplication('https://https://mspi-a4b75.firebaseio.com', None)
    for item in to_be_deleted: 
        storage_client.collection(u'webrtctest').document(item.id).delete()
        
#Camera is not Active -> Alerts database that camera is not ready for use
    active = False
    camera_collection = storage_client.collection('cameras')
    document = camera_collection.document(cameraID) 
    field_updates = {"active": False}
    document.update(field_updates)        
    
#Camera is not Ready -> Alerts database that camera is not ready for use
    ready = False
    field_updates = {"ready": False}
    document.update(field_updates)
    
#--------------------------------------------------------------------------------------------------#  

#Train Face data models
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, 'familiarFaces')

    labels = []
    paths = []

    #Loop through all images in directory
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg") or file.endswith("JPG"):
                path = os.path.join(root, file)
                
                #label comes from file name
                label = file.split(".")[0]
                paths.append(path)
                labels.append(label)

    #Open Images and create encodings
    #loop through Names and add them to known_face_names
    for i in range (0, len(paths)):
        tempImage = face_recognition.load_image_file(paths[i])
        tempEncoding = face_recognition.face_encodings(tempImage)[0]
        known_face_encodings.append(tempEncoding)

    
    
    known_face_names = labels
    
#--------------------------------------------------------------------------------------------------#  
#Set Ready = True on db
    ready = True
    camera_collection = storage_client.collection('cameras')
    document = camera_collection.document(cameraID) 
    field_updates = {"ready": True}
    document.update(field_updates)
    
#Create Doc on database webrtctest
    data = {
        u'sender':cameraID,
        u'what': u'unlock'
        }
    storage_client.collection(u'webrtctest').document().set(data)
 
    
        
