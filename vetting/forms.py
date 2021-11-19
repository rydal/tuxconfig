from vetting.models import VettingDetails, RepositoryURL

from django import forms
from django.forms import inlineformset_factory
from .models import RepoModel, RepositoryURL



class RepositoryURLForm(forms.ModelForm):
    class Meta:
        model = RepositoryURL
        fields = ('discussion_url',)

RepositoryURLFormset = inlineformset_factory(
    RepoModel,
    RepositoryURL,
    fields=["discussion_url",   'id'],
    extra=0,
    can_delete=False

)

class RepoForm(forms.ModelForm):

    discussion_url=forms.URLField()

    class Meta:
        model = RepositoryURL
        fields = ('discussion_url',)

class CreateUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()



class UserDetailsForm(forms.ModelForm):

    class Meta:
        model = VettingDetails
        fields = ('bio','email','website','avatar_url','location',"name","company")

