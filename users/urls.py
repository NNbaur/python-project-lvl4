from django.urls import path
from .views import *

urlpatterns = [
    path('', UserListView.as_view(), name='users_list'),
    path('create/', RegisterUser.as_view(), name='user_add'),
    path('<int:pk>/update/', UpdateUser.as_view(), name='user_update'),
    path('<int:pk>/delete/', DeleteUser.as_view(), name='user_delete'),
]