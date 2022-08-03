from django import forms
from .models import Status

class StatusForm(forms.ModelForm):
    name = forms.CharField(label='Имя',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    class Meta:
        model = Status
        fields = ['name']