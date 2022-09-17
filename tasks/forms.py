from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    name = forms.CharField(label='Имя', error_messages={'unique': 'Задача с таким именем уже существует!'},
                           widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'label']
