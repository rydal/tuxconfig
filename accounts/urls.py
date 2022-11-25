from django.urls import path, include,reverse_lazy
from django.contrib.auth import views as auth_views

from tuxconfig_django import settings
from . import views
from allauth.account.views import SignupView, LoginView, PasswordResetView
from django.conf.urls import url

app_name = "accounts"

urlpatterns = [
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('howitworks/', views.howitworks, name='howitworks'),
    path('privacy/', views.howitworks, name='privacy'),
    path('inception/', views.inception, name='inception'),
    path('landing/', views.inception, name='landing'),
    path('request/', views.inception, name='request'),
    url(r'^logout/$', views.logout_user,  name='logout')
]

