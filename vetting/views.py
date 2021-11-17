import json

from django.shortcuts import render, get_object_or_404

# Create your views here.
from contributor.models import RepoModel
from vetting.forms import RepoForm, UserDetailsForm, RepositoryURLForm
from django.forms import modelformset_factory

from django.contrib.auth.decorators import user_passes_test

from vetting.models import SignedOff, VettingDetails, RepositoryURL

from django.contrib import messages
@user_passes_test(lambda u: u.groups.filter(name='vetting').exists())
def dashboard(request):
    repo_url = RepoModel()
    repo_url_form = RepoForm(instance=repo_url) # setup a form for the parent
    AnswerFormSet = modelformset_factory(model=RepoModel, fields=['discussion_url','id'],
                                         form=RepoForm, extra=False, can_delete=False
                                         )

    formset = RepositoryURLForm(instance=repo_url)

    repos = RepoModel.objects.all().order_by("created")

    if request.POST:
        repo_url_form = RepositoryURLForm(request.POST)
        answer_formset = AnswerFormSet(request.POST)


        if "upvote" in request.POST:
            pk =  request.POST.get("upvote")
            repo_model = RepoModel.objects.get(id=pk)
            repo_model.upvotes = repo_model.upvotes + 1
            try:
                SignedOff.objects.get(contributor=request.user,repo_model=repo_model)
                messages.error(request,"You have already voted on this repository")
            except:
                SignedOff(contributor=request.user,repo_model=repo_model,upvoted=True).save()
                repo_model.save()
        elif "downvote" in request.POST:
            pk =  request.POST.get("downvote")
            repo_model = RepoModel.objects.get(id=pk)
            repo_model.downvotes = repo_model.downvotes + 1
            try:
                SignedOff.objects.get(contributor=request.user,repo_model=repo_model)
                messages.error(request,"You have already voted on this repository")
            except:
                SignedOff(contributor=request.user,repo_model=repo_model,downvoted=True).save()
                repo_model.save()

        if answer_formset.is_valid():
            print ("Answer formset valid")
            for answer in answer_formset:
                id = answer.initial['id']

                try:

                    repository = RepoModel.objects.get(id=id)
                    print(repository)
                    r = RepositoryURL(contributor=request.user,repo_model=repository,discussion_url=answer.cleaned_data.get('discussion_url'))
                    r.save()
                except RepoModel.DoesNotExist:

                    pass
    for repo in repos:
        repo.urls = RepositoryURL.objects.get(repo_model=repo)
    repositories_formset = AnswerFormSet(queryset=repos)

    return render(request,"dashboard.html",{"repositories" : repositories_formset, "repo_url_form" : repo_url_form })

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
            messages.error(request,json.dumps(user_details.errors))
    try:
        vetting_details = VettingDetails.objects.get(user=request.user)
    except VettingDetails.DoesNotExist:
        vetting_details = None
    if vetting_details is not None:
        user_details = UserDetailsForm(instance=vetting_details)
    else:
        user_details = UserDetailsForm()
    return render(request,"vetter_form.html",{"user_details" : user_details })



