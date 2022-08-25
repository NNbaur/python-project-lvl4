from .forms import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class UserListView(ListView):
    model = MyUser
    template_name = 'users/users_list.html'
    context_object_name = 'users_list'


class RegisterUser(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/user_add.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')


class UpdateUser(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = MyUser
    form_class = UserRegistrationForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users_list')
    success_message = _('The user has been successfully changed')
    def test_func(self):
        obj = self.get_object()
        return obj.username == self.request.user.username
    def handle_no_permission(self):
        messages.error(self.request, _('You do not have rights to change this user!'))
        return redirect(reverse_lazy('users_list'))


class DeleteUser(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = MyUser
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users_list')
    error_url = reverse_lazy('users_list')

    def test_func(self):
        obj = self.get_object()
        return obj.username == self.request.user.username

    def handle_no_permission(self):
        messages.error(self.request, _('You do not have permission to delete this user!'))
        return redirect(reverse_lazy('users_list'))

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, _('The user was successfully deleted'))
            return redirect(reverse_lazy('users_list'))
        except ProtectedError:
            messages.error(self.request, _('This user cannot be deleted because it is in use!'))
            return redirect(reverse_lazy('users_list'))
