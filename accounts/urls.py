from django.urls import path, include,reverse_lazy
from django.contrib.auth import views as auth_views

from tuxconfig_django import settings
from . import views
from allauth.account.views import SignupView, LoginView, PasswordResetView
from django.conf.urls import url

app_name = "account"

urlpatterns = [
    path('howitworks/', views.howitworks, name='howitworks'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('contribute/', views.contribute, name='contribute'),
    path('howitworks/', views.howitworks, name='howitworks'),
    url(r'^logout/$', views.logout_user,  name='logout'),

]