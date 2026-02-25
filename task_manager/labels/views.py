from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy
from django.shortcuts import redirect

from .models import Label
from .forms import LabelForm
from task_manager.tasks.models import Task


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'base/list.html'
    context_object_name = 'labels'
    extra_context = {
        'title':'Метки',
        'create_url': 'labels:create',
        'create_button': 'Создать метку',
        'table_headers': ['ID','Имя','Дата создания'],
        'list_title': 'Метки',
        'row_template': 'labels/table_row.html'
    }

class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'base/form.html'
    success_url = reverse_lazy('labels:list')
    extra_context = {
        'title': 'Создать метку',
        'form_title': 'Создать метку',
        'submit_button': 'Создать'        
    }

    def form_valid(self, form):
        messages.success(self.request, gettext_lazy('Метка успешно создана'))
        return super().form_valid(form)

class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'base/form.html'
    success_url = reverse_lazy('labels:list')

    extra_context = {
        'title': 'Изменение метки',
        'form_title': 'Изменение метки',
        'submit_button': 'Изменить'
    }

    def form_valid(self, form):
        messages.success(self.request,gettext_lazy('Метка успешно изменена'))
        return super().form_valid(form)
    
class LabelDeleteView(LoginRequiredMixin, DeleteView):
    
    model = Label
    form = LabelForm
    template_name = 'base/delete.html'
    success_url = reverse_lazy('labels:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Удаление метки',
            'delete_title': 'Удаление метки',
            'delete_message': 'Вы уверены, что хотите удалить метку?',
            'submit_button': 'Да, удалить',
        })
        return context

    def form_valid(self, form):
        messages.success(self.request,gettext_lazy('Метка успешно удалена'))
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if Task.objects.filter(labels=label).exists():
            messages.error(request, gettext_lazy('Невозможно удалить метку, она используется'))
            return redirect('labels:list')
            
        return super().post(request, *args, **kwargs)
        


# Create your views here.
