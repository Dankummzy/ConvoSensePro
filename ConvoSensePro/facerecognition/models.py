from django.db import models
from users.models import User  # Import User model from the Users App

class RecognizedFace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    face_image = models.ImageField(upload_to='recognized_faces/')
    confidence = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - Confidence: {self.confidence}'


