from django.db import models
from django.contrib.auth.models import Group
from django.db.models import UniqueConstraint

from contributor.models import Devices


# Create your models here.

class RequestedDeviceId(models.Model):
    device_id = models.CharField(primary_key=True,max_length=12)

    device = models.ForeignKey(
        Devices,
        related_name="requetsed_device_to_device",
        on_delete=models.CASCADE,
        null=True,
        blank=False
    )
    vote_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class MakeRequest(models.Model):
    pk = models.AutoField(primary_key=True)
    ip = models.GenericIPAddressField(null=False,blank=False)
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
