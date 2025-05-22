from django.db import models

# Create your models here.
from django.db import models

class Camera(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    stream_url = models.URLField()

    def __str__(self):
        return f"{self.name} ({self.location})"
