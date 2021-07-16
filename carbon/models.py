from django.db import models

# Create your models here.
class Carbon(models.Model):
    userid = models.IntegerField()
    carbonfootprint_score = models.IntegerField()

class Citys(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "cities"

class Planting(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)

from django.db import models
from datetime import datetime

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=1000)
class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)