from django.urls import path
from .views import *

urlpatterns = [
    path('users/', UserListView.as_view(), name='users_list'),
    path('users/create/', RegisterUser.as_view(), name='user_add'),
    path('users/<int:pk>/update/', UpdateUser.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', DeleteUser.as_view(), name='user_delete'),
]