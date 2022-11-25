from django.db import models
from django.contrib.auth.models import Group
from django.db.models import UniqueConstraint


# Create your models here.

class RequestedDeviceId(models.Model):
    device_id = models.CharField(max_length=9, primary_key=True)
    version_number = models.SmallIntegerField(default=0)
    vote_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    
        
class DownloadedDeviceId(models.Model):
    device_id = models.CharField(max_length=9, primary_key=True)
    version_number = models.SmallIntegerField(default=0)
    vote_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()