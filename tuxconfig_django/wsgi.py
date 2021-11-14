"""
WSGI config for tuxconfig_django project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from contributor.models import *
from user.models import *
from django.apps import AppConfig

new_group, created = Group.objects.get_or_create(name='github')
permissions_list =  Permission.objects.all()
new_group.permissions.set(permissions_list)

new_group, created = Group.objects.get_or_create(name='google')
permissions_list =  Permission.objects.all()
new_group.permissions.set(permissions_list)


new_group, created = Group.objects.get_or_create(name='stackexchange')
permissions_list =  Permission.objects.all()
new_group.permissions.set(permissions_list)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuxconfig_django.settings')

application = get_wsgi_application()
