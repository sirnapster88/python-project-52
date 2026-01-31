from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserCreateForm, UserUpdateForm

class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'
    ordering = ['id']

class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request,'Пользователь успешно создан! Теперь войдите в систему.')
        return super().form_valid(form)
    
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:list')

    def form_valid(self, form):
        messages.success(self.request,'Пользователь успешно обновлен!')
        return super().form_valid(form)
    
class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request,'Пользователь успешно удален!')
        return super().delete(request, *args, **kwargs)





# Create your views here.
