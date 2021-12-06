import json
import operator
from urllib.request import urlopen

from django.shortcuts import render

from django.db import models
import requests
# Create your models here.
from contributor.models import RepoModel, Devices, Platforms
from tuxconfig_django import settings
from django.http import JsonResponse
import httplib2

from vetting.models import SignedOff, VettingDetails

import ast
from django.contrib import messages

def check_device_exists(request,device_id,platform):
    if device_id is None:
        return JsonResponse({"error" : "device id not set"})
    try:
        devices = RepoModel.objects.filter(device_to_repository__device_id=device_id).select_related()
    except RepoModel.DoesNotExist:
        devices = None

    repositories = []
    for device in devices:
        try:
            Platforms.objects.filter(cpu_hardware_id=platform)
            repositories.append(device)
        except Platforms.DoesNotExist:
            pass

    if len(repositories) == 0:
        return JsonResponse({'none' : True })
    repositories_available = []
    for result in repositories:
        clone_url = "https://github.com/" + result.git_username + "/"  + result.git_repo
        h = httplib2.Http()
        resp = h.request(clone_url, 'HEAD')
        if int(resp[0]['status']) < 400:
            repositories_available.append({"clone_url" : clone_url, "commit" : result.git_commit, "stars" : str(result.stars),"pk" : result.id })
        else:
            return JsonResponse({'error' : "error pulling from github" })

    s = json.dumps(repositories_available)
    s = ast.literal_eval(s)
    return JsonResponse(s,safe=False)



def get_user_details(request,repo_model):
    if repo_model is None:
        return JsonResponse({"error" : "Repo model not set"})
    try:
        model = RepoModel.objects.get(id=repo_model)
    except RepoModel.DoesNotExist:
        model = None
        messages.error(request,"Can't find repository key")
    h = httplib2.Http()
    github_url = "https://api.github.com/users/" + model.git_username
    s = urlopen(github_url)
    respBody = json.loads(s.read())
    try:
        sign_off_object = SignedOff.objects.filter(repo_model=model).order_by("?").first().contributor
    except SignedOff.DoesNotExist:
        sign_off_object = None
        messages.error(request,"Can't find any code vetters")
    try:
        sign_off_user = VettingDetails.objects.get(user=sign_off_object)
    except SignedOff.DoesNotExist:
        sign_off_user = None
        messages.error(request,"Can't find code vetter details")

    return render(request,"get_user_details.html", {"git_user" : respBody, "signed_off_by" : sign_off_user })





