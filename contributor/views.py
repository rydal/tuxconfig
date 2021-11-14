import re

from django.shortcuts import render
import urllib.request, json
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from .models import RepoModel, Devices
from django.contrib import messages

import git
@login_required
def profile(request):
    if request.POST:
        if "repository" in request.POST:
            repo = request.POST['repository']
            s = SocialAccount.objects.get(user_id=request.user.pk)
            try:
                latest_commit = get_latest_commit(s.extra_data['login'],repo.rsplit('/', 1)[-1])
                stored_repo = RepoModel.objects.get(git_url=repo,git_commit=latest_commit['sha'])

                messages.error(request,"Commit already imported.")

            except RepoModel.DoesNotExist:

                latest_commit = get_latest_commit(s.extra_data['login'],repo.rsplit('/', 1)[-1])
                module_config =  check_tuxconfig(s.extra_data['login'],repo.rsplit('/', 1)[-1])
                module = module_config.getModule()
                if module.error is not True:
                    messages.error(request,module.error)
                else:
                    repo_model = RepoModel(contributor=request.user,git_url=repo,git_commit=latest_commit['sha'],upvotes=0,downvotes=0,signed_off=False)
                    repo_model.save()
                    if module.device_ids is not False:
                        for device in module.device_ids:
                            Devices(contributor=request.user,device_id=device,repo_model=repo_model).save()
                        messages.success(request,"Repository imported")
                    else:
                        print (module.device_ids)





    social_id = SocialAccount.objects.get(user_id=request.user.pk)
    git_user_details = social_id.extra_data['url']
    result = get_repos(git_user_details)

    live_repos = RepoModel.objects.filter(contributor=request.user)

    return render(request, "repos.html", {"live_repos" : live_repos , "repo_list" : result })

def get_repos(username):
    print ("USERNAME" + username)
    with urllib.request.urlopen( username + "/repos") as url:
        data = json.loads(url.read().decode())

    return data

def get_latest_commit(owner, repo):

    url = 'https://api.github.com/repos/{owner}/{repo}/commits'.format(owner=owner, repo=repo)
    response = urllib.request.urlopen(url).read()
    data = json.loads(response.decode())
    return data[0]

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def check_tuxconfig(owner,repo):
    url = "https://raw.githubusercontent.com/{owner}/{repo}/master/tuxconfig".format(owner=owner, repo=repo)
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        return "Tuxconfig file does not exist"
    page = str(urllib.request.urlopen(url).read(),"utf-8")
    page = page.replace("\\n","")
    page = page.replace("\"","")
    result = dict(re.findall(r'(\S+)=(".*?"|\S+)', page))
    print (result)
    print (result['device_ids'] + "EH?")
    device_string = result['device_ids']
    module = result['tuxconfig_module']
    dependencies  = result['dependencies']
    restart = result['restart_needed']
    devices = []
    for device in device_string.split(" "):
        devices.append(device)
    module_config = Moduleconfig(devices,module,dependencies,restart)
    return module_config



class Moduleconfig:

    def __init__(self, device_ids, module_id,dependencies,restart):
        self.device_ids = device_ids
        self.module_id = module_id
        self.dependencies = dependencies
        self.restart = restart
        self.error = ""
        if module_id is None:
            self.error = "Device id not defined"
        elif device_ids is None:
            self.error = "Module id not defined"
        else:
            self.error =  True



    def getModule(self):
        return self

