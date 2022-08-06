from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from .forms import *


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'task_list'


class CreateTask(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = TaskForm
    template_name = 'tasks/task_add.html'
    success_url = '/tasks/'
    success_message = 'Задача успешно создана'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateTask, self).form_valid(form)


class UpdateTask(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = '/tasks/'
    success_message = 'Задача успешно изменена'


class DeleteTask(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = '/tasks/'
    success_message = 'Задача успешно удалена'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, 'Задачу может удалить только её автор')
        return redirect('task_list')


class TaskView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_view.html'
