from django.shortcuts import render
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
    template_name = 'labels/list.html'
    context_object_name = 'labels'

class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('label:list')

    def form_valid(self, form):
        messages.success(self.request, gettext_lazy('Метка успешно создана'))
        return super().form_valid(form)

class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/create.html'
    success_url = reverse_lazy('labels:list')

class LabelDeleteView(LoginRequiredMixin, DeleteView):
    
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:list')

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        if Task.objects.filter(labels=label).exists():
            messages.error(request, gettext_lazy('Невозможно удалить метку, она используется'))
            return redirect('labels:list')
            
        return super().post(request, *args, **kwargs)
        


# Create your views here.
