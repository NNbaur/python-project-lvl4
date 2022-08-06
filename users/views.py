from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import MyUser
from django.db.models import ProtectedError
from django.core.exceptions import ImproperlyConfigured
from .forms import *

class UserListView(ListView):
    model = MyUser
    template_name = 'users/users_list.html'
    context_object_name = 'users_list'

class RegisterUser(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/user_add.html'
    success_url = '/login/'
    success_message = 'Пользователь успешно зарегистрирован'

class UpdateUser(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = MyUser
    form_class = UserRegistrationForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно изменен'
    raise_exception = True
    def test_func(self):
        obj = self.get_object()
        return obj.username == self.request.user.username
    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав на изменение данного пользователя!')
        return redirect('users_list')

class DeleteUser(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = MyUser
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users_list')
    error_url = reverse_lazy('users_list')

    def test_func(self):
        obj = self.get_object()
        return obj.username == self.request.user.username

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав на удаление данного пользователя!')
        return redirect('users_list')

    def get_error_url(self):
        if self.error_url:
            return self.error_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured("No error URL to redirect to.")

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, 'Пользователь успешно удален')
            return redirect(reverse_lazy('users_list'))
        except ProtectedError:
            messages.error(self.request, 'Невозможно удалить данного пользователя, потому что он используется!')
            return redirect(reverse_lazy('users_list'))
