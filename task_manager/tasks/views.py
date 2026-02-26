from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy
from django_filters.views import FilterView

from .models import Task
from .forms import TaskForm
from .filters import TaskFilter

class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    template_name = 'base/list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter
    
    def get_filterset_kwargs(self, *args, **kwargs):
        kwargs = super().get_filterset_kwargs(*args, **kwargs)
        kwargs['request'] = self.request
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Задачи',
            'create_url': 'tasks:create',
            'create_button': 'Создать задачу',
            'table_headers': ['ID','Имя','Статус','Автор','Исполнитель','Дата создания',''],
            'list_title': 'Задачи',
            'row_template': 'tasks/table_row.html',
            'filter_form': context['filter'].form,
            'has_filter': bool(self.request.GET),       
            })
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/detail_view.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'base/form.html'
    success_url = reverse_lazy('tasks:list')
    extra_context = {
        'title': 'Создать задачу',
        'form_title': 'Создать задачу',
        'submit_button': 'Создать'       
    }



    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, gettext_lazy('Задача успешно создана'))
        return super().form_valid(form)
    

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'base/form.html'
    success_url = reverse_lazy('tasks:list')
    extra_context = {
        'title': 'Изменение задачи',
        'form_title': 'Изменение задачи',
        'submit_button': 'Изменить'
    }


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'base/delete.html'
    success_url = reverse_lazy('tasks:list')
    extra_context = {
        'title': 'Удаление задачи',
        'delete_title': 'Удаление задачи',
        'delete_message': 'Вы уверены, что хотите удалить задачу',
        'submit_button': 'Да, удалить',
    }

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != request.user:
            messages.error(request, gettext_lazy('Задачу может удалить только ее автор'))
            return redirect('tasks:list')
        return super().post(request, *args, **kwargs)
    

# Create your views here.
