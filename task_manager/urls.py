from django.contrib import admin
from django.urls import path, include

from .views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('task_manager.users.urls')),
    path('', IndexView.as_view(), name='index')
]