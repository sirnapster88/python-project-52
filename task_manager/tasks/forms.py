from django import forms
from django.utils.translation import gettext_lazy
from .models import Task
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']
        labels = {
            'name': gettext_lazy('Имя'),
            'description': gettext_lazy('Описание'),
            'status': gettext_lazy('Статус'),
            'executor': gettext_lazy('Исполнитель')
        }
    