import csv
import uuid, logging, json

from django.contrib.auth.backends import UserModel
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from .models import Profile
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.safestring import SafeString

from allauth.socialaccount.models import SocialAccount

from contributor.views import get_repos
from user_model.models import User
from .forms import UserRegistrationForm, \
    ResendEmailForm, UserLoginForm2
# from org.models import Org, Membership
# from org.forms import OrgForm
from django.core.mail import send_mail, EmailMessage
from django_countries.fields import CountryField

from django.conf import settings

logging.basicConfig(filename='debug.log', level=logging.INFO)
from allauth.account.views import SignupView, LoginView




class MyLoginView(LoginView):
    template_name = 'registration/login.html'
# def UserRegister(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             group = Group.objects.get(name='group_name')
#             user.groups.add(group)
#             return redirect('login')
#     else:
#         form = UserCreationForm()
#     return render(request, 'register/user_register.html', {'form': form})


@login_required
def profile(request):
    if request.user.groups.all()[0].name == "github":
        return redirect("/contributor")
    else:
        return HttpResponse("Invalid user")





# NO login required
def register(request):
    logging.info('view account.register')
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():

            email = user_form.cleaned_data.get('email').lower()
            country = user_form.cleaned_data.get("country")
            password = user_form.cleaned_data.get("password")
            confirm_password = user_form.cleaned_data.get('confirm_passowrd')
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.email = new_user.email.lower()
            new_user.country = country

            new_user.set_password(password)
            # Save the User object
            new_user.save()
            # group = Group.objects.get(name='teacher')
            # new_user.groups.add(group)
            logging.info('Register: Saved new user: ' + str(new_user.id))
            # # Create the new organsiation
            # org = Org.objects.create(name=user_form.cleaned_data['org_name'])
            # logging.info('Register: Saved new org '+org.id.hex)
            # # Join new user to the new org with a membership
            # mem = Membership.objects.create(org=org, user=new_user)
            # logging.info('Register: Saved new membership '+ mem.id.hex)
            # # Set the session org id
            # request.session['oid'] = org.id.hex
            # logging.info('Register: Sessoion oid was set')
            # # Create the user profile
            # referral = None
            # if request.session.get('referral_used'):
            #     # Quick sanity check that the referral link is 12 chars
            #     if len(request.session.get('referral_used')) == 12:
            #         referral = request.session.get('referral_used')
            # Profile.objects.create(user=new_user, default_org=org, referral_used=referral)

            uid = urlsafe_base64_encode(force_bytes(new_user.pk))
            token = default_token_generator.make_token(new_user)
            logging.info("view account.register: /account/activate/" + uid + "/" + token + "/")

            current_site = get_current_site(request)
            mail_subject = 'Computers to schools: Activate your account.'
            message = render_to_string('account/acc_active_email.html', {
                'user': new_user,
                'user_type': new_user.role,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, "support@computerstoschools.co.uk", to=[to_email]
            )
            email.content_subtype = "html"

            email.send()
            messages.success(request, "Registration successful, please check your email.")

            # After a successful registration we do a redirect because that clears
            # the referral link from the URL, we already used the referral link
            return redirect('/account/register/done/')
        else:
            logging.info('Register: Form was not valid: ' + json.dumps(user_form.errors))
            messages.error(request, json.dumps(user_form.errors))
            return render(request,
                          'account/register.html',
                          {
                              'user_form': user_form,
                          })
    user_form = UserRegistrationForm()
    country = CountryField(blank_label='(select country)')
    return render(request,
                  'account/register.html',
                  {
                      'user_form': user_form,
                      "country": country,
                  })


def register_done_view(request):
    messages.info(request, "Registered successfully, please check your email for a verification code.")
    return render(request, 'account/register_done.html')


def activate(request, uidb64, token):
    user = None
    uid = urlsafe_base64_decode(uidb64).decode()
    user = get_object_or_404(User, pk=uid)

    if user is not None and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        return render(request,
                      'account/verified.html',
                      {'success': True})
    else:
        return render(request,
                      'account/verified.html',
                      {'success': False})


def forget(request, uidb64, token):
    user = None
    uid = urlsafe_base64_decode(uidb64).decode()
    try:
        user = User.objects.get(pk=uid)
    except:
        return render(request,
                      'account/forget.html',
                      {'success': False})

    if user is not None and default_token_generator.check_token(user, token):
        user.delete()
        return render(request,
                      'account/forget.html',
                      {'success': True})


def csrf_failure(request, reason=""):
    return render(request, "account/error_page.html")


from allauth.account.signals import user_logged_in
from django.core.signals import request_finished
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import Group

@receiver(user_logged_in)
def login_user(sender, request, user, **kwargs):
    try:
        socialuser = SocialAccount.objects.get(user=user, provider="github")
        group = Group.objects.get(name='github')
        user.groups.add(group)
    except SocialAccount.DoesNotExist:
        pass




