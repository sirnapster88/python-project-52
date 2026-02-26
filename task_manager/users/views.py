from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import UserCreateForm, UserUpdateForm


class UserListView(ListView):
    model = User
    template_name = 'base/list.html'
    context_object_name = 'users'
    ordering = ['id']
    extra_context = {
        'title':'Пользователи',
        'table_headers': ['ID','Имя пользователя','Полное имя','Дата создания',''],
        'list_title': 'Пользователи',
        'row_template': 'users/table_row.html'
    }

class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateForm
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
    form_class = UserUpdateForm
    template_name = 'base/form.html'
    success_url = reverse_lazy('users:list')
    extra_context = {
        'title': 'Изменение пользователя',
        'form_title': 'Изменение пользователя',
        'submit_button': 'Изменить'
    }
    success_message = 'Пользователь успешно изменен'

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'base/delete.html'
    success_url = reverse_lazy('users:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
        'title': 'Удаление пользователя',
        'delete_title': 'Удаление пользователя',
        'delete_message': f'Вы уверены, что хотите удалить {self.object.username}?',
        'submit_button': 'Да, удалить'
        })
        return context

    def post(self, request, *args, **kwargs):
        messages.success(request,'Пользователь успешно удален!')
        return super().delete(request, *args, **kwargs)

# Create your views here.
