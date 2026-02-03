from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from .models import Status
from .forms import StatusForm

class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/list.html'
    ordering = ['name']

    
class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses:list')

    login_url = reverse_lazy('login')

    
class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses:list')

    login_url = reverse_lazy('login')

    
class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    form = StatusForm
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:list')

    login_url = reverse_lazy('login')

    
# Create your views here.
