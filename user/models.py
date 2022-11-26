from django.db import models
from django.contrib.auth.models import Group
from django.db.models import UniqueConstraint

from contributor.models import Devices


# Create your models here.

class RequestedDeviceId(models.Model):
    device_id = models.CharField(primary_key=True,max_length=12)
    vote_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()
