from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError

from .forms import StatusForm
from .models import Status
from task_manager.tasks.models import Task


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'
    ordering = ['name']
    extra_context = {
        'title': 'Статусы',
        'list_title': 'Статусы',
        'create_button': 'Создать статус'
    }


class StatusCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'base/form.html'
    success_url = reverse_lazy('statuses:list')

    login_url = reverse_lazy('login')
    extra_context = {
        'title': 'Создать статус',
        'form_title': 'Создать статус',
        'submit_button': 'Создать'
    }
    success_message = 'Статус успешно создан.'


class StatusUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'base/form.html'
    success_url = reverse_lazy('statuses:list')

    login_url = reverse_lazy('login')
    extra_context = {
        'title': 'Изменение статуса',
        'form_title': 'Изменение статуса',
        'submit_button': 'Изменить'
    }
    success_message = 'Статус успешно изменен'


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    form = StatusForm
    template_name = 'base/delete.html'
    success_url = reverse_lazy('statuses:list')
    login_url = reverse_lazy('login')
    extra_context = {
            'title': 'Удаление статуса',
            'delete_title': 'Удаление статуса',
            'submit_button': 'Да, удалить',
        }

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, 'Статус успешно удален')
            return response
        except ProtectedError:
            messages.error(request, 'Нельзя удалить статус')
            return redirect('statuses:list')


# Create your views here.
