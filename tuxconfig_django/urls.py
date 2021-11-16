"""tuxconfig_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.conf.urls.static import static

import accounts.views
from tuxconfig_django import settings

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    path('social/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', accounts.views.index),
    path('contributor/', include('contributor.urls')),
    path('user/', include('user.urls')),
    path('vetting/', include('vetting.urls')),

] + static( settings.STATIC_URL, document_root=settings.STATIC_ROOT)


