from .models import Label
from .forms import LabelForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'label_list'


class CreateLabel(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = LabelForm
    template_name = 'labels/label_add.html'
    success_url = reverse_lazy('label_list')
    success_message = _('Label created successfully')


class UpdateLabel(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_update.html'
    success_url = reverse_lazy('label_list')
    success_message = _('Label changed successfully')


class DeleteLabel(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('label_list')
    success_message = _('Label deleted successfully')

    def post(self, request, *args, **kwargs):
        try:
            self.delete(request, *args, **kwargs)
            messages.success(self.request, _('Label deleted successfully'))
            return redirect(reverse_lazy('label_list'))
        except ProtectedError:
            messages.error(self.request, _('This label cannot be deleted because it is in use!'))
            return redirect(reverse_lazy('label_list'))
