from django import forms
from .models import Status
from django.utils.translation import gettext

class StatusForm(forms.ModelForm):
    name = forms.CharField(label='Имя', error_messages={'unique': 'Статус с таким именем уже существует!'} ,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))

    class Meta:
        model = Status
        fields = ['name']