from django.template.defaulttags import url

from .views import SignUpView, CabinetView
from django.urls import path
import django.contrib.auth.views

urlpatterns = [
    #path('password_change/', PasswordChangeView.as_view(), name='password_change_form'),
    path('singup/', SignUpView.as_view(), name='singup'),
    path('cabinet/', CabinetView.as_view(), name='cabinet')
]