import django_filters
from django import forms
from django.contrib.auth import get_user_model

from task_manager.labels.models import Label

from .models import Status, Task

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
        field_name='labels',
        label='Метка',
        distinct=True
    )

    my_task = django_filters.BooleanFilter(
        method='filter_my_task',
        widget=forms.CheckboxInput,
        label='Только мои задачи'
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'my_task']

    def filter_my_task(self, queryset, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset
