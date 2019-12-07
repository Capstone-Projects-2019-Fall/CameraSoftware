#-------------------------------------------------------------------------------#
#Import Libraries
import time
import os
import settings

#-------------------------------------------------------------------------------#
#Initialize Global Variables
settings.init()

#-------------------------------------------------------------------------------#
#import modules
from object_detection import detect_object
from recordOnMotion import detect_motion
#-------------------------------------------------------------------------------#


os.system("sudo pkill x")

# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot, changes, read_time):
    
    for change in changes:
        if change.type.name == 'ADDED':
            if(change.document.to_dict().get('what') == 'lock'):
                print('LOCKED')
                settings.lock = True
                settings.unlock = False
   
            if(change.document.to_dict().get('what') == 'unlock'):
                print('UNLOCKED')
                os.system("pkill chromium")
                settings.unlock = True
                settings.lock = False
                
        if change.type.name == 'MODIFIED':
            if(change.document.to_dict().get('active') == False):
                settings.active = False
            if(change.document.to_dict().get('active') == True):
                settings.active = True

storage_client = settings.firestore.client()

#Watchers
col_query_lock = storage_client.collection(u'webrtctest').where(u'what', u'==', u'lock').where(u'target', u'==', settings.cameraID)
col_query_unlock = storage_client.collection(u'webrtctest').where(u'what', u'==', u'unlock').where(u'sender', u'==', settings.cameraID)
col_query_camera_status = storage_client.collection(u'cameras').document(settings.cameraID)
    
query_watch_camera_status = col_query_camera_status.on_snapshot(on_snapshot)
query_watch_lock = col_query_lock.on_snapshot(on_snapshot)
query_watch_unlock = col_query_unlock.on_snapshot(on_snapshot)


#Camera warms up
time.sleep(2)

#Infinite Loop
while True:
    #Master loop
    if settings.active is True:
        #Loop will start upon camera activation
        while settings.active is True:
            #Camera functions
            while settings.lock is False and settings.active is True:
                if settings.lock == False and settings.active == True:
                    print("Object recognition Called")
                    #time.sleep(5)
                    detect_object()
                if settings.lock == False and settings.active == True:
                    print("Video Started")
                    #time.sleep(5)
                    detect_motion(16)
                    print("Video Ended")
            
            
            print("LOCKED")
            firstTime = True
            
            #Live Streaming
            while settings.unlock is False and settings.active is True:
                #col_query_unlock.on_snapshot(on_snapshot)
                if firstTime:
                    print("Started WebRTC")
                    firstTime = False
                    os.system("chromium-browser localhost")
      
            print("stopping webRTC")
            
            
            
    
    

