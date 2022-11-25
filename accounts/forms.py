import logging

from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from user_model.models import User
from django_countries.widgets import CountrySelectWidget



class UserLoginForm2(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    #user_type = forms.CharField(label='Donating a computer or sending one?', widget=forms.RadioSelect(choices=CHOICES),                                required=True)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password','country')
    field_order = ['email', 'password','confirm_password','country']

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

        try:
            password_validation.validate_password(password, self.instance)
        except forms.ValidationError:
            raise forms.ValidationError(
                "Password too simple"
            )



class ResendEmailForm(forms.Form):
    email = forms.EmailField(label='Email address')