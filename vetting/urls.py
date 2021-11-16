from django.urls import path, include,reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from allauth.account.views import SignupView, LoginView, PasswordResetView
from django.conf.urls import url



app_name = "vetting"

urlpatterns = [
    url('', views.dashboard, name='profile'),

]