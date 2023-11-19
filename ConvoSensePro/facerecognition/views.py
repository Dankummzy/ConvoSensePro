import cv2
import os
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.conf import settings
from events.models import Event
from attendance.models import AttendanceRecord
from users.models import User
import face_recognition
import numpy as np
import pickle
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# Configuration paths
MODELS_DIR = os.path.join(settings.BASE_DIR, 'facerecognition', 'models')
trained_encodings_path = os.path.join(MODELS_DIR, 'encodings.pkl')

# Load known faces and their names
known_face_encodings = []
known_face_names = []

with open(trained_encodings_path, "rb") as f:
    data = pickle.load(f)
    known_face_encodings, known_face_names = data

# Your code to load known faces goes here

def process_and_mark_attendance(event, user_id):
    user = User.objects.get(pk=user_id)
    try:
        attendance_record = AttendanceRecord.objects.get(event=event, user=user)
        if attendance_record.present:
            return f"{user.username} is already marked present."
        attendance_record.present = True
        attendance_record.save()
        return f"{user.username}'s attendance has been recorded!"
    except AttendanceRecord.DoesNotExist:
        attendance_record = AttendanceRecord(event=event, user=user, present=True)
        attendance_record.save()
        return f"{user.username}'s attendance has been recorded!"

@require_POST
@csrf_exempt
def start_face_recognition(request, event_id):
    event_id = int(event_id)
    event = Event.objects.get(pk=event_id)

    video_capture = cv2.VideoCapture(0)

    process_this_frame = True

    while True:
        ret, frame = video_capture.read()
        if process_this_frame:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                recognized_name = "Unknown"
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    recognized_name = known_face_names[best_match_index]

                if recognized_name != "Unknown":
                    try:
                        # Look up the user based on the recognized name
                        user = User.objects.get(username=recognized_name)
                        response = process_and_mark_attendance(event, user.id)
                        # You can add further handling of the response as needed

                        # Append the recognized name to the face_names list
                        face_names.append(recognized_name)
                    except User.DoesNotExist:
                        # Handle the case where the recognized name does not match a user
                        pass

            # Draw recognized names on the frame for each face
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  # Increase bounding box size
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        process_this_frame = not process_this_frame

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

    return HttpResponse("Recognition started successfully")
