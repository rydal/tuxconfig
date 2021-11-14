from django.shortcuts import render

from django.db import models

# Create your models here.
from contributor.models import RepoModel, Devices
from tuxconfig_django import settings
from django.http import JsonResponse

def check_device_exists(request):
    device_id = request.GET['device_id']
    version = request.GET['version']
    available_devices = Devices.objects.filter(device_id=device_id).order_by("repo_model__upvotes")
    result = available_devices[version]
    if result.signed_off:
        return JsonResponse({'url': result.git_url, "commit_id" : result.git_commit })
    else:
        return JsonResponse({'none' : True })

def profile(request):
    return render(request,"profile.html")


