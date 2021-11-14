from django.urls import path, include,reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = "user"
urlpatterns = [
    path("", views.profile, name="profile"),
    path("get_device/", views.check_device_exists, name="check_device"),
]
