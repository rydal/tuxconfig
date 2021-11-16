from django.urls import path, include,reverse_lazy
from django.contrib.auth import views as auth_views
from . import views
from allauth.account.views import SignupView, LoginView, PasswordResetView
from django.conf.urls import url
class MySignupView(SignupView):
    template_name = 'registration/login.html'

class MyLoginView(LoginView):
    template_name = 'registration/login.html'

class MyPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_done.html'

app_name = "account"

urlpatterns = [
    path('howitworks/', views.howitworks, name='howitworks'),

]