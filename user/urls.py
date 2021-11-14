from django.urls import path, include,reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from allauth.account.views import SignupView, LoginView, PasswordResetView
from django.conf.urls import url

app_name = "user"

urlpatterns = [
    url('profile', views.profile, name='profile'),
    path('get_device/<str:device_id>/<int:version>/', views.check_device_exists, name='check_device'),

]