from django.db import models

# Create your models here.

class TheImages(models.Model):
    image = models.ImageField(upload_to='img/')