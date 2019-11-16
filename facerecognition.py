import face_recognition
import os

def recognizeFace():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, 'familiarFaces')

    labels = []
    paths = []

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


    #loop through Names and add them to known_face_names
    #Load Picture to be compared


    known_face_encodings= []

    for i in range (0, len(paths)):
        tempImage = face_recognition.load_image_file(paths[i])
        tempEncoding = face_recognition.face_encodings(tempImage)[0]
        known_face_encodings.append(tempEncoding)

    known_face_names = labels

    # Load test image to find faces in
    test_image = face_recognition.load_image_file('./img/groups/group1.jpg')

    # Find faces in test image
    face_locations = face_recognition.face_locations(test_image)
    face_encodings = face_recognition.face_encodings(test_image, face_locations)


    # Loop through faces in test image
    for(top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    name = "Unknown Person"

    # If match
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]
        print(name)
