import os
import face_recognition

def init():
#Initializer
   
    #Globals
    global lock
    global unlock
    global cameraID
    global known_face_encodings
    global known_face_names
    global userID
    global active
    global ready
    
    cameraID = "00123"
    lock = False
    unlock = True
    known_face_encodings = []
    active = False
    ready = False
    
    #Download all pics from
    #Get Camera user
    #setup paths for webRTC
    #setup paths to pictures and videos
    #Listen for activation
    #Send Ready Signal
    
    #Setup FireBase Credentials
    
    
    
    #Train Face data models
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, 'familiarFaces')

    labels = []
    paths = []

    print("Looping through images...")
    #Loop through all images in directory
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg") or file.endswith("JPG"):
                path = os.path.join(root, file)
                
                #label comes from folder name
            
                label = file.split(".")[0]
                paths.append(path)
                labels.append(label)

    #Open Images and create encodings


    print("Paths retrieved: ", paths)

    print("Labels Retrieved", labels)

    #loop through Names and add them to known_face_names
    #Load Picture to be compared

    for i in range (0, len(paths)):
        tempImage = face_recognition.load_image_file(paths[i])
        tempEncoding = face_recognition.face_encodings(tempImage)[0]
        known_face_encodings.append(tempEncoding)

    
    
    known_face_names = labels
