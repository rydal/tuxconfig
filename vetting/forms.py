from django import forms

from contributor.models import RepoModel
from tuxconfig_django import settings


class SignOffForm(forms.ModelForm):

    class Meta:
        model = RepoModel
        fields = ("git_url", "git_commit", "module_name","upvotes", "downvotes")

class UserSignOffForm(forms.ModelForm):

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ("")
