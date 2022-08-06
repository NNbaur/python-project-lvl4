from django.urls import path
from .views import *

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', CreateTask.as_view(), name='task_add'),
    path('tasks/<int:pk>/update/', UpdateTask.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', DeleteTask.as_view(), name='task_delete'),
    path('tasks/<int:pk>', TaskView.as_view(), name='task_view'),
]