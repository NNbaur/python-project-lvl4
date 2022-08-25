from .forms import *
from .filters import TaskFilter
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django_filters.views import FilterView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'task_list'
    login_url = 'login'
    filterset_class = TaskFilter


class CreateTask(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'tasks/task_add.html'
    success_url = reverse_lazy('task_list')
    success_message = _('Task created successfully')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateTask, self).form_valid(form)


class UpdateTask(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('task_list')
    success_message = _('Task changed successfully')


class DeleteTask(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('task_list')
    success_message = _('Task deleted successfully')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, _('Only the author can delete a task'))
        return redirect(reverse_lazy('task_list'))


class TaskView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_view.html'
