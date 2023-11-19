# myapp/management/commands/train_face_recognition.py

import os
import face_recognition
import pickle
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Train the face recognition model'

    def handle(self, *args, **options):
        known_faces_dir = os.path.join(settings.MEDIA_ROOT, 'user_faces')
        MODELS_DIR = os.path.join(settings.BASE_DIR, 'facerecognition', 'models')
        trained_encodings_path = os.path.join(MODELS_DIR, 'encodings.pkl')

        known_face_encodings = []
        known_face_names = []

        for username in os.listdir(known_faces_dir):
            user_dir = os.path.join(known_faces_dir, username)
            if os.path.isdir(user_dir):
                for filename in os.listdir(user_dir):
                    if filename.endswith('.jpg'):
                        image_path = os.path.join(user_dir, filename)
                        try:
                            image = face_recognition.load_image_file(image_path)
                            face_locations = face_recognition.face_locations(image, model="cnn")

                            if face_locations:
                                face_encodings = face_recognition.face_encodings(image, face_locations)

                                if len(face_encodings) > 0:
                                    for face_encoding in face_encodings:
                                        known_face_encodings.append(face_encoding)
                                        known_face_names.append(username)
                                else:
                                    print(f"No face found in {image_path}")
                            else:
                                print(f"No face found in {image_path}")
                        except Exception as e:
                            print(f"Error processing {image_path}: {e}")

        try:
            with open(trained_encodings_path, 'wb') as file:
                pickle.dump((known_face_encodings, known_face_names), file)
            print("Saved encodings to encodings.pkl")
        except Exception as e:
            print(f"Error while saving encodings: {e}")



