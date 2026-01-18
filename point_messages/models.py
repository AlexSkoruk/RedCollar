from django.db import models
from django.conf import settings
from points.models import Point

class Message(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} @ {self.point}"