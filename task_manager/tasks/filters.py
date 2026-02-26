import django_filters
from django import forms
from .models import Task, Status
from task_manager.labels.models import Label
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        queryset=Status.objects.all(),
        field_name='status_id',
        label='Статус'
    )

    executor = django_filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='executor_id',
        label='Исполнитель'
    )

    label = django_filters.ModelChoiceFilter(
        queryset=Label.objects.all(),
        field_name='labels__id',
        label='Метка',
        distinct=True
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

