from django import forms
from django.utils.translation import gettext_lazy
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
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
            'labels':gettext_lazy('Метки')
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].required = False
        self.fields['status'].queryset = Status.objects.all()
        self.fields['executor'].queryset = User.objects.all()
        self.fields['labels'].queryset = Label.objects.all()
        self.fields['executor'].label_from_instance = self._user_label
        self.fields['executor'].empty_label = '---------'
        self.fields['status'].empty_label = '---------'
