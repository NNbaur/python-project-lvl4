from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from users.forms import *
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

class HomePage(TemplateView):
    template_name = 'greet.html'

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    next_page = 'home'
    success_message = _('You have successfully logged in')
    def form_invalid(self, form):
        messages.error(self.request, _('Please enter the correct username and password. Both fields can be case sensitive.'))
        return redirect(reverse_lazy('login'))

class UserLogoutView(LogoutView):
    next_page = 'home'