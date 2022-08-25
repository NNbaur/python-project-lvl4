from django.urls import path
from .views import *

urlpatterns = [
    path('', StatusListView.as_view(), name='status_list'),
    path('create/', CreateStatus.as_view(), name='status_add'),
    path('<int:pk>/update/', UpdateStatus.as_view(), name='status_update'),
    path('<int:pk>/delete/', DeleteStatus.as_view(), name='status_delete'),
]