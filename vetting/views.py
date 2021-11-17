import json

from django.shortcuts import render, get_object_or_404

# Create your views here.
from contributor.models import RepoModel
from vetting.forms import RepoForm, UserDetailsForm
from django.forms import modelformset_factory

from django.contrib.auth.decorators import user_passes_test

from vetting.models import SignedOff, VettingDetails

from django.contrib import messages
@user_passes_test(lambda u: u.groups.filter(name='vetting').exists())
def dashboard(request):

    repos = RepoModel.objects.all().order_by("created")
    AnswerFormSet = modelformset_factory(model=RepoModel, fields=['discussion_url'],
                                         form=RepoForm, extra=False, can_delete=False
                                         )
    if request.POST:
        answer_formset = AnswerFormSet(request.POST)
        print (answer_formset)

        if "upvote" in request.POST:
            pk =  request.POST.get("upvote")
            repo_model = RepoModel.objects.get(id=pk)
            repo_model.upvotes = repo_model.upvotes + 1
            SignedOff(contributor=request.user,repo_model=repo_model,upvoted=True).save()
            repo_model.save()
        elif "downvote" in request.POST:
            pk =  request.POST.get("downvote")
            repo_model = RepoModel.objects.get(id=pk)
            repo_model.downvotes = repo_model.downvotes + 1
            SignedOff(contributor=request.user,repo_model=repo_model,downvoted=True).save()
            repo_model.save()
        elif answer_formset.is_valid():

            for answer_form in answer_formset:
                    print("VALID")
                    if answer_form.is_valid():
                        answer_form.save()
                    else:

                        messages.error(request,json.dumps(answer_formset.errors))

    repositories_formset = AnswerFormSet(queryset=repos)
    return render(request,"dashboard.html",{"repositories" : repositories_formset })

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



