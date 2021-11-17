import re

from django.shortcuts import render
import urllib.request, json
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount

from tuxconfig_django import settings
from .models import RepoModel, Devices
from django.contrib import messages
import  requests
from django.contrib.auth.decorators import user_passes_test

@login_required
def profile(request):
    if request.POST:
        if "add_repository" in request.POST:
            repo = request.POST['add_repository']
            s = SocialAccount.objects.get(user_id=request.user.pk)
            try:
                latest_commit = get_latest_commit(s.extra_data['login'],repo.rsplit('/', 1)[-1])
                RepoModel.objects.get(contributor=request.user,git_repo=repo,git_commit=latest_commit['sha'])

                messages.error(request,"Commit already imported.")

            except RepoModel.DoesNotExist:

                latest_commit = get_latest_commit(s.extra_data['login'],repo.rsplit('/', 1)[-1])
                module_config , error =  check_tuxconfig(s.extra_data['login'],repo.rsplit('/', 1)[-1])
                git_repo = repo.rsplit('/', 1)[-1]
                if error is not None:
                    messages.error(request,error)
                else:
                    repo_model = RepoModel(contributor=request.user,git_repo=git_repo,git_username=s.extra_data['login'],git_commit=latest_commit['sha'],module_name=module_config.module_id,upvotes=0,downvotes=0,stars=module_config.stars,signed_off=False)
                    repo_model.save()
                    for device in module_config.device_ids:
                        Devices(contributor=request.user,device_id=device,repo_model=repo_model).save()
                    messages.success(request,"Repository imported")

    if "delete_repository" in request.POST:
        id = request.POST['delete_repository']
        s = SocialAccount.objects.get(user_id=request.user.pk)
        try:
            repo = RepoModel.objects.get(contributor=request.user,id=id)
            commit_id = repo.git_commit
            commit_name = repo.git_repo
            repo.delete()

            messages.success(request, commit_name + " " + commit_id + " deleted.")

        except RepoModel.DoesNotExist:
            messages.error(request,"Repository not found")





    social_id = SocialAccount.objects.get(user_id=request.user.pk)
    git_user_details = social_id.extra_data['url']
    result = get_repos(git_user_details)

    live_repos = RepoModel.objects.filter(contributor=request.user)
    for repo in live_repos:
        repo.devices =  Devices.objects.filter(repo_model=repo)
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
    error = None
    if "device_ids" in result:
        device_string = result['device_ids']
    else:
        error = "device_ids not present"
        return None, error
    if "module_id" in result:
        module = result['module_id']
    else:
        error = "tuxconfig_module not present"
        return None, error
    if "dependencies" in result:
        dependencies  = result['dependencies']
    else:
        error = "dependencies not present"
        return None, error
    if "version" in result:
        version = result['version']
    else:
        error = "Version not present"
        return None, error

    stars = get_stars(owner,repo)
    if stars < settings.MIN_STARS:
        error = "Need at least 20 stars to be submitted to our program"
        return None, error
    devices = []
    if error is not None:
        return None, error
    else:
        for device in device_string.split(" "):
            device = device.strip(" ")
            if not re.findall("[0-9a-zA-Z]{4}:[0-9a-zA-Z]{4}",device):
                error = "Device id must be of format nnnn:nnnn"
                return None, error
            devices.append(device)
        module_config = Moduleconfig(devices,module,dependencies,version,stars)
        return module_config , None



def get_stars(owner,repo):
    r = requests.get("https://api.github.com/repos/" + owner + "/" + repo)
    result = r.json()
    return result['stargazers_count']

class Moduleconfig:

    def __init__(self, device_ids, module_id,dependencies,version,stars):
        self.device_ids = device_ids
        self.module_id = module_id
        self.dependencies = dependencies
        self.version = version
        self.stars = stars






    def getModule(self):
        return self

