import csv
import uuid, logging, json

# from org.models import Org, Membership
# from org.forms import OrgForm
from django.core.mail import send_mail, EmailMessage
from django_countries.fields import CountryField

from django.conf import settings

logging.basicConfig(filename='debug.log', level=logging.INFO)
from allauth.account.views import SignupView, LoginView





from allauth.account.signals import user_logged_in
from django.core.signals import request_finished
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


@receiver(user_logged_in)
def login_user(sender, request, user, **kwargs):
    try:
        socialuser = SocialAccount.objects.get(user=user, provider="github")
        group = Group.objects.get(name='github')
        user.groups.add(group)
    except SocialAccount.DoesNotExist:
        pass



@login_required
def profile(request):
    if request.user.groups.all()[0].name == "github":
        return redirect("/contributor")
    elif request.user.groups.all()[0].name == "vetting":
        return redirect("/vetting")
    else:
        return HttpResponse("Invalid user")




from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def logout_user(request):
    response = HttpResponseRedirect(reverse('index.html'))
    return response


def privacy(request):
    return None


def howitworks(request):
    return None

def index(request):
    return render(request,"index.html")

def login(request):
    return  redirect("/social/login")