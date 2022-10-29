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

from vetting.models import SignedOff, VettingDetails

import ast

from user.forms import DownloadedIdForm


def check_device_exists(request,device_id):
    if device_id is None:
        return JsonResponse({"error" : "device id not set"})

    devices = Devices.objects.filter(device_id=device_id).select_related()
    repositories = []
    for device in devices:
         repositories.append(device.repo_model)  # You already have it
    if len(repositories) == 0:
        return JsonResponse({'none' : True })
    repositories_available = []
    for result in repositories:
        clone_url = "https://github.com/" + result.git_username + "/"  + result.git_repo + "/commit/" + result.git_commit
        h = httplib2.Http()
        resp = h.request(clone_url, 'HEAD')
        if int(resp[0]['status']) < 400:
            repositories_available.append({"clone_url" : clone_url, "stars" : str(result.stars),"pk" : result.id })

    s = json.dumps(repositories_available)
    s = ast.literal_eval(s)
    return JsonResponse(s,safe=False)



def get_user_details(request,repo_model):
    if repo_model is None:
        return JsonResponse({"error" : "Repo model not set"})
    model = RepoModel.objects.get(id=repo_model)
    github_url = "https://api.github.com/users/" + model.git_username
    s = urlopen(github_url)
    respBody = json.loads(s.read())
    downloaded_from = DownloadedIdForm(request.POST or None)
    if request.POST:
        if downloaded_from.is_valid():
            downloaded_from.save()
    return render(request,"get_user_details.html", {"git_user" : respBody, "model" : model, "form": downloaded_from })




