import logging

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from user_model.models import User
from django_countries.widgets import CountrySelectWidget

