from django import forms

from contributor.models import RepoModel
from vetting.models import VettingDetails


class RepoForm(forms.ModelForm):
    id = forms.HiddenInput()
    discussion_url=forms.URLField()

    class Meta:
        model = RepoModel
        fields = ('discussion_url',"id")


class UserDetailsForm(forms.ModelForm):

    class Meta:
        model = VettingDetails
        fields = ('bio','email','website','avatar_url','location',"name","company")

