from django.urls import path, include,reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = "contributor"
urlpatterns = [
    path("", views.profile, name="profile"),
    path("devices_sought/", views.ShowRequestedDevices.as_view(), name="devices_sought"),

]
