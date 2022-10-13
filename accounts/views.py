import csv
import uuid, logging, json

# from org.models import Org, Membership
# from org.forms import OrgForm
from django.core.mail import send_mail, EmailMessage
from django_countries.fields import CountryField

from django.conf import settings

logging.basicConfig(filename='debug.log', level=logging.INFO)
from allauth.account.views import SignupView, LoginView
from django.contrib.auth import logout

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








from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request,"accounts/index.html")

def profile(request):
    return render(request,"contributor:profile")

def privacy(request):
    return render(request,"accounts:privacy")


def howitworks(request):
    return render(request,"accounts:howitworks")

def index(request):
    return render(request, "accounts/index.html")

def login(request):
    return  redirect("/social/login")