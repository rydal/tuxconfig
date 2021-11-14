from django.shortcuts import render

from django.db import models

# Create your models here.
from contributor.models import RepoModel, Devices
from tuxconfig_django import settings
from django.http import JsonResponse

from user.page_rank import GetPR


def check_device_exists(request):
    device_id = request.GET['device_id']
    version = request.GET['version']

    repositories = Devices.objects.filter(device_id=device_id)._meta.get_field('repo_model').related_model
    GetPR


    clone_url = result.git_url + "/commit/" + result.git_commit
    if result.signed_off:
        return JsonResponse({'clone_url': result.git_url, "user_details" : result.contributor, "none" : False })
    else:
        return JsonResponse({'none' : True })

def profile(request):
    return render(request,"profile.html")


