from django.contrib.auth.views import LoginView
from django.shortcuts import render

from .forms import UserLoginForm


# Create your views here.
TEMPLATES = {
    'login': 'authenticate/login.html'
}


class UserLoginView(LoginView):
    template_name = 'authenticate/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form'] = UserLoginForm()

        return context
