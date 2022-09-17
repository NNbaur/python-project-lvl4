from .models import Status
from .forms import StatusForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses_list'


class CreateStatus(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = StatusForm
    template_name = 'statuses/status_add.html'
    success_url = reverse_lazy('status_list')
    success_message = _('Status created successfully')


class UpdateStatus(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_update.html'
    success_url = reverse_lazy('status_list')
    success_message = _('Status changed successfully')


class DeleteStatus(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('status_list')
    success_message = _('Status deleted successfully')

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, _('Status deleted successfully'))
            return redirect(reverse_lazy('status_list'))
        except ProtectedError:
            messages.error(self.request, _('This status cannot be deleted because it is in use!'))
            return redirect(reverse_lazy('status_list'))
