from django.shortcuts import render

# Create your views here.
from contributor.models import RepoModel
from django.forms import formset_factory

from vetting.forms import SignOffForm


def SignOff(request):
    repos = RepoModel.objects.filter(signed_off=False).order_by("created")
    SignOffFormSet = formset_factory(SignOffForm)
    formset = SignOffFormSet(queryset=repos)

    return render(request,{ "reposFormSet",formset } )
