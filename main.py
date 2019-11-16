#-------------------------------------------------------------------------------#
#Import Libraries
import time
import settings
import firebase_admin
from firebase import firebase
from firebase_admin import credentials
from firebase_admin import storage
from google.cloud import firestore
from firebase_admin import firestore

#-------------------------------------------------------------------------------#

#Initialize Global Variables
settings.init()

#INITIALIZE FIREBASE APP
cred=credentials.Certificate('/home/pi/Desktop/CameraSoftware/cred.json')
#cred=credentials.Certificate('cred.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'mspi-a4b75.appspot.com'
})
storage_client = firestore.client()
#-------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------#
#import modules
from object_detection import detect_object
from recordOnMotion import detect_motion
#-------------------------------------------------------------------------------#


# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot, changes, read_time):
    
    for change in changes:
        print(u'New city: {}'.format(change.document.to_dict().get('what')))
        if change.type.name == 'ADDED':
            if(change.document.to_dict().get('what') == 'lock'):
                print('LOCK DOC')
                settings.lock = True
                settings.unlock = False
            if(change.document.to_dict().get('what') == 'unlock'):
                print('UNLOCK DOC')
                settings.unlock = True
                settings.lock = False


#Watchers
col_query_lock = storage_client.collection(u'webrtctest').where(u'what', u'==', u'lock')
col_query_unlock = storage_client.collection(u'webrtctest').where(u'what', u'==', u'unlock')
query_watch = col_query_lock.on_snapshot(on_snapshot)
query_watch2 = col_query_unlock.on_snapshot(on_snapshot)

#Camera warms up
time.sleep(2)

#Main infinite loop
while True:
    #Camera functions
    while settings.lock is False:    
        if settings.lock == False:
            print("Object recognition Called")
            #time.sleep(5)
            detect_object()
        if settings.lock == False:
            print("Video Started")
            #time.sleep(5)
            detect_motion(32)
            print("Video Ended")
    
    
    print("LOCKED")
    firstTime = True
    
    #Live Streaming
    while settings.unlock is False:
        #col_query_unlock.on_snapshot(on_snapshot)
        if firstTime:
            print("Started WebRTC")
            firstTime = False
           

       
            
    print("stopping webRTC")
        
        
    
    

