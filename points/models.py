from django.contrib.gis.db import models

class Point(models.Model):
    title = models.CharField(max_length=255, blank=True)  
    location = models.PointField(srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Point ({self.location.y}, {self.location.x})"