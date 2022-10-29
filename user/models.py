from django.db import models
from django.contrib.auth.models import Group
# Create your models here.
from tuxconfig_django import settings

class RequestedDeviceId(models.Model):
    device_id = models.CharField(max_length=9, primary_key=True)
    version_number = models.SmallIntegerField(primary_key=True,default=0)
    vote_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class DownloadedDeviceId(models.Model):
    device_id = models.CharField(max_length=9, primary_key=True)
    version_number = models.SmallIntegerField(primary_key=True,default=0)
    vote_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()