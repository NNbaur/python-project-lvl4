from django.urls import path
from .views import TaskListView, CreateTask, UpdateTask, DeleteTask, TaskView, excel_csv

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list'),
    path('create/', CreateTask.as_view(), name='task_add'),
    path('<int:pk>/update/', UpdateTask.as_view(), name='task_update'),
    path('<int:pk>/delete/', DeleteTask.as_view(), name='task_delete'),
    path('<int:pk>', TaskView.as_view(), name='task_view'),
    path('excel_csv', excel_csv, name='excel_csv'),
]
