from django.db import models

# Create your models here
class Reservation(models.Model):
        username = models.CharField(max_length = 50, default = '')
        startTime = models.DateTimeField()
        endTime = models.DateTimeField()
