from django.db import models

# Create your models here.
from contributor.models import RepoModel
from tuxconfig_django import settings


class SignedOff(models.Model):
    contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="signed_off_to_user",
        on_delete=models.CASCADE,
    )
    id = models.AutoField(primary_key=True)
    repo_model = models.ForeignKey(
        RepoModel,
        related_name="contributor_to_repo_model",
        on_delete=models.CASCADE,
    )
    device_id = models.CharField(max_length=12)
    created = models.DateTimeField(auto_now_add=True)
    upvoted = models.BooleanField(default=False)
    downvoted = models.BooleanField(default=False)
    objects = models.Manager()

class RepositoryURL(models.Model):
    contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="repository_url_to_user",
        on_delete=models.CASCADE,
    )
    id = models.AutoField(primary_key=True)
    repo_model = models.ForeignKey(
        RepoModel,
        related_name="repository_url_to_repo",
        on_delete=models.CASCADE,
    )
    discussion_url = models.CharField(max_length=240)


class VettingDetails(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="vetter_to_user",
        on_delete=models.CASCADE,
    )
    id = models.AutoField(primary_key=True)
    bio = models.CharField(max_length=240)
    email = models.EmailField(max_length=240)
    website = models.URLField(max_length=240)
    avatar_url = models.URLField(max_length=240)
    location = models.CharField(max_length=120)
    name = models.CharField(max_length=80)
    company = models.CharField(max_length=120)
