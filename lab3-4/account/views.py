from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import  User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    #reverse_lazy, чтобы перенаправить пользователя
    # на страницу входа в систему после успешной регистрации
    success_url = reverse_lazy('login')
    template_name = 'singup.html'

class CabinetView(generic.View):
    def get(self, request, *args, **kwargs):

        return render(request, 'cabinet.html')
