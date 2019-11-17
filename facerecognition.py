import settings

settings.init()

faces_recognized = []

while True:
    print("START")

    # Load test image to find faces in
    test_image = settings.face_recognition.load_image_file('/home/pi/Desktop/CameraSoftware/WhoDat.jpg')

     # Find faces in test image
    face_locations = settings.face_recognition.face_locations(test_image)
    face_encodings = settings.face_recognition.face_encodings(test_image, face_locations)


    print("Images Encoded...")
    # Loop through faces in test image
    for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = settings.face_recognition.compare_faces(settings.known_face_encodings, face_encoding)
        print("Face Rec started...")
        name = "Unknown Person"

        # If match
        if True in matches:
            first_match_index = matches.index(True)
            name = settings.known_face_names[first_match_index]
            faces_recognized.append(name)
            
    for face in faces_recognized:
        print(face)
        
    #FUTURE:
    #return faces_recognize
            


