from django.db import models
from django.contrib.auth.models import Group
# Create your models here.
from tuxconfig_django import settings


class RepoModel(models.Model):
    contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="contributor_to_user",
        on_delete=models.CASCADE,
    )
    id = models.AutoField(primary_key=True)
    git_repo = models.CharField(max_length=240)
    git_commit = models.CharField(max_length=240)
    git_username = models.CharField(max_length=240)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    discussion_url = models.URLField(max_length=240,null=True,blank=True)
    signed_off = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    stars = models.PositiveIntegerField(default=0)
    module_name = models.CharField(max_length=40,null=True)
    module_version = models.CharField(max_length=40,null=True)
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
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Platforms(models.Model):
    contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="platform_to_contributor",
        on_delete=models.CASCADE,
    )
    id = models.AutoField(primary_key=True)
    repo_model = models.ForeignKey(
        RepoModel,
        related_name="platform_to_repository",
        on_delete=models.CASCADE,
    )
    cpu_hardware_id = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()