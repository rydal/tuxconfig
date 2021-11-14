from django.shortcuts import render

from django.db import models
import requests
# Create your models here.
from contributor.models import RepoModel, Devices
from tuxconfig_django import settings
from django.http import JsonResponse
import httplib2


def check_device_exists(request,device_id,version):
    if device_id is None:
        return JsonResponse({"error" : "device id not set"})
    if version is None:
        return JsonResponse({"error" : "version required not set"})

    devices = Devices.objects.filter(device_id=device_id)
    if len(devices) == 0:
        return JsonResponse({'none' : True })
    repositories = []
    for device in devices:
        repo = device._meta.get_field('repo_model').related_model
        repo.stars = get_stars(repo.git_username,repo.git_repo)
        repositories.append(repo)
    result = repositories[version]
    clone_url = result.git_url + "/commit/" + result.git_commit
    h = httplib2.Http()
    resp = h.request(clone_url, 'HEAD')
    if int(resp[0]['status']) < 400:
        return JsonResponse({'clone_url': result.git_url, "user_details" : result.contributor, "none" : False })
    else:
        return JsonResponse({'none' : True })

def profile(request):
    return render(request,"profile.html")

