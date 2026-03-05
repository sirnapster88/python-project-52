from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView

from .filters import TaskFilter
from .forms import TaskForm
from .models import Task


class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter
    extra_context = {
        'title': 'Задачи',
        'list_title': 'Задачи'
    }


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail_view.html'
    context_object_name = 'task'


class TaskCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'base/form.html'
    success_url = reverse_lazy('tasks:list')
    extra_context = {
        'title': 'Создать задачу',
        'form_title': 'Создать задачу',
        'submit_button': 'Создать'
    }
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'base/form.html'
    success_url = reverse_lazy('tasks:list')
    extra_context = {
        'title': 'Изменение задачи',
        'form_title': 'Изменение задачи',
        'submit_button': 'Изменить'
    }
    success_message = 'Задача успешно изменена'


class TaskDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'base/delete.html'
    success_url = reverse_lazy('tasks:list')
    extra_context = {
        'title': 'Удаление задачи',
        'delete_title': 'Удаление задачи',
        'delete_message': 'Вы уверены, что хотите удалить задачу',
        'submit_button': 'Да, удалить',
    }
    success_message = 'Задача успешно удалена'

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, 'Задачу может удалить только ее автор')  # noqa:E501
            return redirect('tasks:list')
        return super().post(request, *args, **kwargs)


# Create your views here.
