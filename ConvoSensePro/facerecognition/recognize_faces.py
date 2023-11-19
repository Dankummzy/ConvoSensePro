import os
import pickle
import face_recognition
from events.models import Event
from attendance.models import AttendanceRecord
from .models import RecognizedFace
from django.conf import settings

MODELS_DIR = os.path.join(settings.BASE_DIR, 'facerecognition', 'models')
trained_encodings_path = os.path.join(MODELS_DIR, 'encodings.pkl')

def recognize_attendance(event, image):
    known_face_encodings, known_face_names = load_known_encodings(trained_encodings_path)

    
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image, face_locations)
    
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            user_id = int(name)
            record_attendance(event, user_id)

def load_known_encodings(file_path):
    known_encodings = []
    known_names = []
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            known_encodings, known_names = pickle.load(file)

    return known_encodings, known_names


def record_attendance(event, user_id, confidence, face_image):
    # Create or update attendance record for the user and event
    try:
        attendance_record = AttendanceRecord.objects.get(event=event, user=user_id)
        attendance_record.present = True
    except AttendanceRecord.DoesNotExist:
        attendance_record = AttendanceRecord(event=event, user=user_id, present=True)
    
    attendance_record.save()
    
    # Save the recognized face and associated data
    recognized_face = RecognizedFace(user_id=user_id, confidence=confidence)
    recognized_face.face_image.save(f'user_{user_id}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.jpg', face_image)
    recognized_face.save()
