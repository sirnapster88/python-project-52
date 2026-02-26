from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class IndexView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

class MessageLoginView(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    next_page = reverse_lazy('index')
    success_message = 'Вы залогинены'

class MessageLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        messages.success(request, 'Вы разлогинены')
        return super().post(request, *args, **kwargs)
