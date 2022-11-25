from django.urls import path, include,reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from allauth.account.views import SignupView, LoginView, PasswordResetView
from django.conf.urls import url

app_name = "user"

urlpatterns = [
    path('get_contributor/<int:repo_model>/', views.get_user_details, name='get_user_details'),
    path('get_device/<str:device_id>/<str:platform>', views.check_device_exists, name='check_device'),

]