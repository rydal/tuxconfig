from django import forms
from captcha.fields import ReCaptchaField
from django.core.exceptions import ValidationError

from .models import RequestedDeviceId, DownloadedDeviceId


class RequestedIdForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaField())

    class Meta:
        model = RequestedDeviceId
        fields = ('device_id','version_number')

    def clean(self):
        version_number = self.cleaned_data.get("version_number")
        device_id = self.cleaned_data.get("device_id")
        if len(device_id) != 9:
            raise ValidationError({"device_id","Not a valid device ID"})
        if version_number > 10:
            raise ValidationError({"version_number","Not a valid version number"})

    def save(self, commit=False):
        version_number = self.cleaned_data.get("version_number")
        device_id = self.cleaned_data.get("device_id")
        try:
            requested_model = RequestedDeviceId.objects.get(version_number=version_number,device_id=device_id)
            requested_model.vote_count = requested_model.vote_count + 1
            requested_model.save()
        except RequestedDeviceId.DoesNotExist:
            RequestedDeviceId(version_number=version_number,device_id=device_id).save()


class DownloadedIdForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaField())

    class Meta:
        model = DownloadedDeviceId
        fields = ('device_id','version_number')

    def clean(self):
        version_number = self.cleaned_data.get("version_number")
        device_id = self.cleaned_data.get("device_id")
        if len(device_id) != 9:
            raise ValidationError({"device_id","Not a valid device ID"})
        if version_number > 10:
            raise ValidationError({"version_number","Not a valid version number"})

    def save(self, commit=False):
        version_number = self.cleaned_data.get("version_number")
        device_id = self.cleaned_data.get("device_id")
        try:
            requested_model = DownloadedIdForm.objects.get(version_number=version_number,device_id=device_id)
            requested_model.vote_count = requested_model.vote_count + 1
            requested_model.save()
        except DownloadedIdForm.DoesNotExist:
            DownloadedDeviceId(version_number=version_number,device_id=device_id).save()





