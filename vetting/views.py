from django.shortcuts import render, get_object_or_404

# Create your views here.
from contributor.models import RepoModel
from vetting.forms import RepoForm, UserDetailsForm
from django.forms import modelformset_factory

from django.contrib.auth.decorators import user_passes_test

from vetting.models import SignedOff, VettingDetails


@user_passes_test(lambda u: u.groups.filter(name='vetting').exists())
def dashboard(request):
    repos = RepoModel.objects.filter(upvotes__lt=4 ).order_by("created")
    AnswerFormSet = modelformset_factory(model=RepoModel, fields=['discussion_url'],
                                         form=RepoForm, extra=False, can_delete=False
                                         )
    if request.POST:
        answer_formset = AnswerFormSet(request.POST)

        if answer_formset.is_valid():
            for answer_form in answer_formset:
                git_repo = answer_form.cleaned_data.get("git_repo")
                git_username = answer_form.cleaned_data.get("git_username")
                git_commit = answer_form.cleaned_data.get("git_commit")
                repo_model = RepoModel.objects.get(git_repo=git_repo,git_username=git_username,git_commit=git_commit)
                repo_model.discussion_url = answer_form.cleaned_data.get("discussion_url")
                repo_model.save()
        else:
            pass
        if "upvote" in request.POST:
            pk =  request.POST.get("upvote")
            repo_model = RepoModel.objects.get(id=pk)
            repo_model.upvotes = repo_model.upvotes + 1
            SignedOff(contributor=request.user,repo_model=repo_model,upvoted=True).save()
            repo_model.save()
        if "downvote" in request.POST:
            pk =  request.POST.get("downvote")
            repo_model = RepoModel.objects.get(id=pk)
            repo_model.downvotes = repo_model.downvotes + 1
            SignedOff(contributor=request.user,repo_model=repo_model,downvoted=True).save()
            repo_model.save()


    repositories_formset = AnswerFormSet(queryset=repos)
    return render(request,"dashboard.html",{"repositories" : repositories_formset })


def add_user_details(request):
    vetting_details = VettingDetails.objects.get(user=request.user)
    if request.POST:
        user_details = UserDetailsForm(request.POST)

        if user_details.is_valid():
             vetting_user = user_details.save(commit=False)
             vetting_user.user = request.user
             user_details.save()
        else:
            print("form not valid")
    if vetting_details is not None:
        user_details = UserDetailsForm(instance=vetting_details)
    else:
        user_details = UserDetailsForm()
    return render(request,"dashboard.html",{"user_details" : user_details })



