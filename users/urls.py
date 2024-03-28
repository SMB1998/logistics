# En tu_app/urls.py
from django.urls import path
from .views import create_user, read_user, update_user, delete_user, login_view

urlpatterns = [
     path('users/', create_user, name='create_user'), 
    path('users/<int:user_id>/', read_user, name='read_user'),
    path('users/<int:user_id>/', update_user, name='update_user'),
    path('users/<int:user_id>/', delete_user, name='delete_user'),
    path('login/', login_view, name='login'),
]
