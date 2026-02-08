from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


from .views import IndexView,MessageLogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('task_manager.users.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', MessageLogoutView.as_view(next_page="/"), name='logout'),
    path('statuses/',include('task_manager.statuses.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('', IndexView.as_view(), name='index')
]