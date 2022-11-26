import json
import operator
from urllib.request import urlopen

import certifi
import urllib3
from django.shortcuts import render

from django.db import models
import requests
from django.views.decorators.http import require_http_methods
from urllib3 import request

# Create your models here.
from contributor.models import RepoModel, Devices
from tuxconfig_django import settings
from django.http import JsonResponse
import httplib2


import ast

from user.forms import DownloadedIdForm
from user.models import RequestedDeviceId, MakeRequest


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


def get_recaptcha_token(token,remote_ip):
        http = urllib3.PoolManager(ca_certs=certifi.where())
        recaptcha_url = 'https://www.google.com/recaptcha/api/siteverify'
        payload = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': token,
            'remoteip': remote_ip,
        }
        encoded_data = json.dumps(payload).encode('utf-8')
        req = http.request('POST', recaptcha_url, payload=encoded_data,headers={'Content-Type': 'application/json'})

        result = json.loads(req.data.decode('utf-8'))['json']
        return result.get('success', False)

def get_client_ip(request):
    x_forwarded_for = request.META.get('X-Forwarded-For')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

from datetime import datetime, timedelta
@require_http_methods(['POST'])
def check_device_available(request):
    if not settings.DEVELOPMENT_MODE and "recaptcha_token" not in request.POST:
        return JsonResponse({"error": "No recaptcha token sent"})
    elif not settings.DEVELOPMENT_MODE and get_recaptcha_token(request.POST['recaptcha_token'],get_client_ip(request)) is False:
        return JsonResponse({"error": "Invalid recaptcha token sent"})
    if "devices_requested" not in request.POST:
        return JsonResponse({"error": "No device list sent"})
    else:
        device_string = request.POST['devices_requested']
        devices = json.loads(device_string)
        repositories_available = []
        now = datetime.now()
        now_minus_10 = now - timedelta(days = 1)

        for device in devices:
            device_already, created = RequestedDeviceId.objects.update_or_create(device_id=device.id)
            MakeRequest.objects.filter(ip=get_client_ip(request)).exists()
            if device_already is not None and created is True and not MakeRequest.objects.filter(ip=get_client_ip(request),created__lte=now_minus_10).exists():
                try:
                    repo_exists = Devices.objects.get(device_id=device.id)
                    device_already.device = repo_exists
                except Devices.DoesNotExist:
                    pass
                device_already.vote_count = device.vote_count + 1
                device_already.save()
            if not Devices.objects.filter(device_id__in=devices).select_related().exists():
                return JsonResponse({'none' : True })
            devices = Devices.objects.filter(device_id__in=devices).select_related()

        for device in devices:
            if settings.CHECK_REPO_STILL_ON_GITHUB:
                clone_url = "https://github.com/" + device.repo_model.git_username + "/"  + device.repo_model.git_repo + "/commit/" + device.repo_model.git_commit
                h = httplib2.Http()
                resp = h.request(clone_url, 'HEAD')
                if int(resp[0]['status']) < 400:
                    repositories_available.append({"device_id" : device.id,"clone_url" : clone_url, "stars" : str(device.repo_model.stars),"pk" : device.repo_model.id })
            else:
                repositories_available.append({"device_id" : device.id,"clone_url" : device.repo_model.clone_url, "stars" : str(device.repo_model.stars),"pk" : device.repo_model.id })
        s = json.dumps(repositories_available)
        s = ast.literal_eval(s)
        return JsonResponse(s,safe=False)
