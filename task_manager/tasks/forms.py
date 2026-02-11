from django import forms
from django.utils.translation import gettext_lazy
from .models import Task
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor','labels']
        labels = {
            'name': gettext_lazy('Имя'),
            'description': gettext_lazy('Описание'),
            'status': gettext_lazy('Статус'),
            'executor': gettext_lazy('Исполнитель'),
            'labels':gettext_lazy('Метка')
        }


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        empty_label='---------',
        label="Статус"
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        empty_label='---------',
        label="Исполнитель"
    )
    label = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        empty_label='---------',
        label="Метка"
    )
    my_task = forms.BooleanField(
        label="Только свои задачи",
        required=False
    )
    