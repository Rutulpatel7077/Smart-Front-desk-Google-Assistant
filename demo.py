import json
from pprint import pprint
import face_recognition
import cv2


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("rutul.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

mark_image = face_recognition.load_image_file("mark.jpg")
mark_face_encoding = face_recognition.face_encodings(mark_image)[0]

barry_image = face_recognition.load_image_file("barry.jpg")
barry_face_encoding = face_recognition.face_encodings(barry_image)[0]

venus_image = face_recognition.load_image_file("venus.jpg")
venus_face_encoding = face_recognition.face_encodings(venus_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    mark_face_encoding,
    barry_face_encoding,
    venus_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Rutul Patel",
    "Mark Yaraskavitch",
    "Barry Morwood",
    "Venus Vavadiya",
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
all_time_faces_names = []
Unknown_array = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame,number_of_times_to_upsample=2)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        with open('data.json') as data_file:
            data_item = json.load(data_file)
            decision = data_item["call_assistant"]
            data_file.close()

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            # Add all names to array for displaying on the screen
            face_names.append(name)
            # if person is unknown then add that to the unknow array for counting total number of unknown people
            if name == "Unknown" and decision == "True":
                Unknown_array.append(name)
            # else filter duplicate names and add those to the final array
            else:
                if name not in all_time_faces_names:
                    all_time_faces_names.append(name)

    process_this_frame = not process_this_frame

    #Fire the ChatBot to talk with unknown people
    if len(Unknown_array) > 10 and decision == "True":
        Unknown_array = []

        data_item["call_assistant"] = "False"

        data_file = open("data.json", "w+")
        data_file.write(json.dumps(data_item))
        data_file.close()


        print("Fire the Google chat assistant")



    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
