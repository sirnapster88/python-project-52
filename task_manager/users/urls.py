from django.urls import path, include
from .views import UserListView, UserCreateView, UserDeleteView, UserUpdateView

app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='list'),
    path('create/', UserCreateView.as_view(), name='create'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='delete'),
]