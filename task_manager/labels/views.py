from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError

from .forms import LabelForm
from .models import Label


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'
    extra_context = {
        'title': 'Метки',
        'list_title': 'Метки'
    }


class LabelCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'base/form.html'
    success_url = reverse_lazy('labels:list')
    extra_context = {
        'title': 'Создать метку',
        'form_title': 'Создать метку',
        'submit_button': 'Создать'
    }
    success_message = 'Метка успешно создана'
    

class LabelUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'base/form.html'
    success_url = reverse_lazy('labels:list')

    extra_context = {
        'title': 'Изменение метки',
        'form_title': 'Изменение метки',
        'submit_button': 'Изменить'
    }
    success_message = 'Метка успешно изменена'
    

class LabelDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):

    model = Label
    form = LabelForm
    template_name = 'base/delete.html'
    success_url = reverse_lazy('labels:list')

    extra_context = {
            'title': 'Удаление метки',
            'delete_title': 'Удаление метки',
            'delete_message': 'Вы уверены, что хотите удалить метку?',
            'submit_button': 'Да, удалить',
        }
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Метка успешно удалена')
            return response
        except ProtectedError:
            messages.error(self.request, 'Невозможно удалить метку')
            return redirect('labels:list')

# Create your views here.
