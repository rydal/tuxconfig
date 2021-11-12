from django.db import models

# Create your models here.
from tuxconfig_django import settings


class RepoModel(models.Model):
    contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="points_to_user",
        on_delete=models.CASCADE,
    )
    id = models.AutoField(primary_key=True)
    git_url = models.CharField(max_length=240)
    git_commit = models.CharField(max_length=240)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    signed_off = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    module_name = models.CharField(max_length=40,null=True)
    objects = models.Manager()

class Devices(models.Model):
    contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="device_to_contributor",
        on_delete=models.CASCADE,
    )
    id = models.AutoField(primary_key=True)
    repo_model = models.ForeignKey(
        RepoModel,
        related_name="device_to_repository",
        on_delete=models.CASCADE,
    )
    device_id = models.CharField(max_length=12)
