import json

from django.shortcuts import render, get_object_or_404

# Create your views here.
from contributor.models import RepoModel
from user_model.models import User
from vetting.forms import RepoForm, UserDetailsForm, RepositoryURLForm, CreateUserForm
from django.forms import modelformset_factory

from django.contrib.auth.decorators import user_passes_test, login_required

from vetting.models import SignedOff, VettingDetails, RepositoryURL

from django.contrib import messages
from django.http import JsonResponse


@user_passes_test(lambda u: u.groups.filter(name='vetting').exists())
def dashboard(request):
    repo_url = RepoModel()
    repo_url_form = RepoForm(instance=repo_url)  # setup a form for the parent
    AnswerFormSet = modelformset_factory(model=RepoModel, fields=['discussion_url', 'id'],
                                         form=RepoForm, extra=False, can_delete=False
                                         )

    formset = RepositoryURLForm(instance=repo_url)

    repos = RepoModel.objects.all().order_by("created")

    if request.POST:
        repo_url_form = RepositoryURLForm(request.POST)
        answer_formset = AnswerFormSet(request.POST)

        if "upvote" in request.POST:
            pk = request.POST.get("upvote")
            repo_model = RepoModel.objects.get(id=pk)
            repo_model.upvotes = repo_model.upvotes + 1
            try:
                SignedOff.objects.get(contributor=request.user, repo_model=repo_model)
                messages.error(request, "You have already voted on this repository")
            except:
                SignedOff(contributor=request.user, repo_model=repo_model, upvoted=True).save()
                repo_model.save()
        elif "downvote" in request.POST:
            pk = request.POST.get("downvote")
            repo_model = RepoModel.objects.get(id=pk)
            repo_model.downvotes = repo_model.downvotes + 1
            try:
                SignedOff.objects.get(contributor=request.user, repo_model=repo_model)
                messages.error(request, "You have already voted on this repository")
            except:
                SignedOff(contributor=request.user, repo_model=repo_model, downvoted=True).save()
                repo_model.save()

    for repo in repos:
        repo.entry_set = RepositoryURL.objects.filter(repo_model=repo)
    try:
        vetting_details = VettingDetails.objects.get(user=request.user)
    except VettingDetails.DoesNotExist:
        vetting_details = None
        messages.info(request,"Please enter your details to be recommended on our systems as a code vetter,")
    return render(request, "dashboard.html", {"repositories": repos,"vetting_details" : vetting_details })


@user_passes_test(lambda u: u.groups.filter(name='vetting').exists())
def add_user_details(request):
    if request.POST:
        user_details = UserDetailsForm(request.POST)

        if user_details.is_valid():
            try:
                vetting_details = VettingDetails.objects.get(user=request.user)
                vetting_details.bio = user_details.cleaned_data.get("bio")
                vetting_details.website = user_details.cleaned_data.get("website")
                vetting_details.email = user_details.cleaned_data.get("email")
                vetting_details.avatar_url = user_details.cleaned_data.get("avatar_url")
                vetting_details.location = user_details.cleaned_data.get("location")
                vetting_details.company = user_details.cleaned_data.get("company")
                vetting_details.name = user_details.cleaned_data.get("name")
                vetting_details.save()
            except VettingDetails.DoesNotExist:
                vetting_user = user_details.save(commit=False)
                vetting_user.user = request.user
                vetting_user.save()
        else:
            messages.error(request, json.dumps(user_details.errors))
    try:
        vetting_details = VettingDetails.objects.get(user=request.user)
    except VettingDetails.DoesNotExist:
        vetting_details = None
    if vetting_details is not None:
        user_details = UserDetailsForm(instance=vetting_details)
    else:
        user_details = UserDetailsForm()
    return render(request, "vetter_form.html", {"user_details": user_details})

from django.http import HttpResponse

@login_required
def account_edit(request):
    form = CreateUserForm()
    if request.user.is_superuser: # just using request.user attributes
        if request.POST:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password")
                try:
                    User.objects.get(email=email)
                    messages.error(request,"User already exists")
                except User.DoesNotExist:
                    u = User.objects.create_user(email,password)
                    u.save()
                    messages.success(request,"User created")
            else:
                messages.error(request,"Form not valid")



        return render(request,"create_user_form.html",{"form" : form })
    else:
        return HttpResponse(request,"Not a superuser")
