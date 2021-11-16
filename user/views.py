import json
import operator
from urllib.request import urlopen

from django.shortcuts import render

from django.db import models
import requests
# Create your models here.
from contributor.models import RepoModel, Devices
from tuxconfig_django import settings
from django.http import JsonResponse
import httplib2

from vetting.models import SignedOff


def check_device_exists(request,device_id,version):
    if device_id is None:
        return JsonResponse({"error" : "device id not set"})
    if version is None:
        return JsonResponse({"error" : "version required not set"})

    devices = Devices.objects.filter(device_id=device_id).select_related()
    repositories = []
    for device in devices:
         repositories.append(device.repo_model)  # You already have it
    if len(repositories) == 0:
        return JsonResponse({'none' : True })

    result = repositories[version]
    clone_url = "https://github.com/" + result.git_username + "/"  + result.git_repo + "/commit/" + result.git_commit
    h = httplib2.Http()
    resp = h.request(clone_url, 'HEAD')
    if int(resp[0]['status']) < 400:
        return JsonResponse({'clone_url': clone_url, "repo_model" : result.pk, "none" : False })
    else:
        return JsonResponse({'none' : True })


def get_user_details(request,repo_model):
    if repo_model is None:
        return JsonResponse({"error" : "Repo model not set"})
    model = RepoModel.objects.get(id=repo_model)
    h = httplib2.Http()
    github_url = "https://api.github.com/users/" + model.git_username
    s = urlopen(github_url)
    respBody = json.loads(s.read())



    sign_off_user = SignedOff.objects.filter(repo_model=model).order_by("?").first()

    return render(request,"get_user_details.html", {"git_user" : respBody, "signed_off_by" : sign_off_user })





