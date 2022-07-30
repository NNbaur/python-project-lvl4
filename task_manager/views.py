from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from users.forms import *
from django.shortcuts import redirect

class HomePage(TemplateView):
    template_name = 'greet.html'

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    next_page = '/'
    success_message = 'Вы успешно вошли в систему'
    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')
        return redirect('/login/')

class UserLogoutView(LogoutView):
    next_page = '/'