from django import forms
from .models import Label


class LabelForm(forms.ModelForm):
    name = forms.CharField(label='Имя', error_messages={'unique': 'Метка с таким именем уже существует!'},
                           widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))

    class Meta:
        model = Label
        fields = ['name']
