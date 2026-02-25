from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext
from django.urls import reverse_lazy
from django.db.models.deletion import ProtectedError
from .models import Status
from .forms import StatusForm

class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'base/list.html'
    ordering = ['name']
    extra_context = {
            'title': 'Статусы',
            'create_url': 'statuses:create',
            'create_button': 'Создать статус',
            'table_headers': ['ID','Имя','Дата создания',''],
            'list_title': 'Статусы',
            'row_template': 'statuses/table_row.html'
        }
    

    
class StatusCreateView(LoginRequiredMixin, CreateView):
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

    def form_valid(self, form):
        messages.success(self.request, gettext('Статус успешно создан.'))
        return super().form_valid(form)

    
class StatusUpdateView(LoginRequiredMixin, UpdateView):
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
    
    def form_valid(self, form):
        messages.success(self.request, gettext('Статус успешно изменён'))
        return super().form_valid(form)
    
class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    form = StatusForm
    template_name = 'base/delete.html'
    success_url = reverse_lazy('statuses:list')

    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Удаление статуса',
            'delete_title': 'Удаление статуса',
            'delete_message': f'Вы уверены, что хотите удалить "{self.object.name}"?',
            'submit_button': 'Да, удалить',
        })
        return context

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request,gettext('Статус успешно удален'))
            return response
        except ProtectedError:
            messages.error(request, gettext('Невозможно удалить статус, потому что он используется'))
            return redirect('statuses:list')

    
# Create your views here.
