from django.urls import path, include,reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from allauth.account.views import SignupView, LoginView, PasswordResetView
from django.conf.urls import url
class MySignupView(SignupView):
    template_name = 'registration/login.html'

class MyLoginView(LoginView):
    template_name = 'registration/login.html'

class MyPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_done.html'

app_name = "account"

urlpatterns = [
    url(r'^login', MyLoginView.as_view(), name='login'),
    url(r'^signup', MySignupView.as_view(), name='signup'),
    url(r'^profile', views.profile, name='profile'),

]