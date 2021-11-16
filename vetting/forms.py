from django import forms

from contributor.models import RepoModel
from vetting.models import VettingDetails


class RepoForm(forms.ModelForm):
    id = forms.HiddenInput()
    upvotes = forms.IntegerField(disabled=True)
    downvotes = forms.IntegerField(disabled=True)
    git_commit = forms.CharField(disabled=True)
    git_url = forms.CharField(disabled=True)
    git_username = forms.CharField(disabled=True)
    module_name = forms.CharField(disabled=True)

    class Meta:
        model = RepoModel
        fields = ('discussion_url',"upvotes","downvotes","git_commit","git_username","git_url","module_name","id")


class UserDetailsForm(forms.ModelForm):

    class Meta:
        model = VettingDetails
        fields = ('bio','email','website','avatar_url','location',"name","company")

