import settings
import cv2
from ttictoc import TicToc
#Create timer
timer = TicToc()

def recognize_faces():
    
    faces_recognized = []
    #Start Timer
    timer.tic()
    
    # Load test image to find faces in
    test_image = settings.face_recognition.load_image_file('/home/pi/Desktop/CameraSoftware/WhoDat.jpg')
    
    # Resize frame of video to 1/2 size for faster face recognition processing
    small_frame = cv2.resize(test_image, (0, 0), fx=0.50, fy=0.50)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    
     # Find faces in test image
    face_locations = settings.face_recognition.face_locations(rgb_small_frame)
    face_encodings = settings.face_recognition.face_encodings(rgb_small_frame, face_locations)

    # Loop through faces in test image
    for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = settings.face_recognition.compare_faces(settings.known_face_encodings, face_encoding)
        name = "Unknown Person"

        # If match
        if True in matches:
            first_match_index = matches.index(True)
            name = settings.known_face_names[first_match_index]
            faces_recognized.append(name)
        else:
            faces_recognized.append(name)
            
    print(timer.toc())
        
    return faces_recognized
            


