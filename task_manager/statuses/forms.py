from django import forms
from django.utils.translation import gettext_lazy
from .models import Status

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {'Имя': 'Имя'}