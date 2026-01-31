from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.contrib import messages


class IndexView(TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html') 
    

class MessageLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы разлогинены')
        return super().dispatch(request, *args, **kwargs)
