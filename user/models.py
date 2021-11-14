from django.db import models
from django.contrib.auth.models import Group
# Create your models here.
from contributor.models import RepoModel
from tuxconfig_django import settings

class Vote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="vote_to_user",
        on_delete=models.CASCADE,
    )
    id = models.AutoField(primary_key=True)
    repo_model = models.ForeignKey(
        RepoModel,
        related_name="user_to_repository",
        on_delete=models.CASCADE,
    )
    upvoted = models.BooleanField(default=False)
    downvoted = models.BooleanField(default=False)
    unsure = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class TwoWeekVote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="two_week_vote_to_user",
        on_delete=models.CASCADE,
    )
    id = models.AutoField(primary_key=True)
    repo_model = models.ForeignKey(
        RepoModel,
        related_name="two_week_user_to_repository",
        on_delete=models.CASCADE,
    )
    upvoted = models.BooleanField(default=False)
    downvoted = models.BooleanField(default=False)
    unsure = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
