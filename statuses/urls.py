from django.urls import path
from .views import *

urlpatterns = [
    path('statuses/', StatusListView.as_view(), name='status_list'),
    path('statuses/create/', CreateStatus.as_view(), name='status_add'),
    path('statuses/<int:pk>/update/', UpdateStatus.as_view(), name='status_update'),
    path('statuses/<int:pk>/delete/', DeleteStatus.as_view(), name='status_delete'),
]