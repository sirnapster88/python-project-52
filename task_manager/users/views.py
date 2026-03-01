from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect

from .forms import UserForm


class UserListView(ListView):
    model = User
    template_name = 'base/list.html'
    context_object_name = 'users'
    ordering = ['id']
    extra_context = {
        'title': 'Пользователи',
        'list_title': 'Пользователи',
        'table_headers': 'users/table_headers.html',
        'row_template': 'users/table_row.html'
    }


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'base/form.html'
    success_url = reverse_lazy('login')
    extra_context = {
        'title': 'Регистрация',
        'form_title': 'Регистрация',
        'submit_button': 'Зарегистрировать'
    }
    success_message = 'Пользователь успешно зарегистрирован'


class UserUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'base/form.html'
    success_url = reverse_lazy('users:list')
    extra_context = {
        'title': 'Изменение пользователя',
        'form_title': 'Изменение пользователя',
        'submit_button': 'Изменить'
    }
    success_message = 'Пользователь успешно изменен'


class UserDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'base/delete.html'
    success_url = reverse_lazy('users:list')
    extra_context = {
        'title': 'Удаление пользователя',
        'delete_title': 'Удаление пользователя',
        'submit_button': 'Да, удалить'
        }
    
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, 'Пользователь успешно удален')
            return response
        except ProtectedError:
            messages.error(request, 'Невозможно удалить пользователя, потому что он является автором или исполнителем задач')  # noqa: E501
            return redirect('users:list')

# Create your views here.
