from django.urls import path
from .views import *

urlpatterns = [
    path('', LabelListView.as_view(), name='label_list'),
    path('create/', CreateLabel.as_view(), name='label_add'),
    path('<int:pk>/update/', UpdateLabel.as_view(), name='label_update'),
    path('<int:pk>/delete/', DeleteLabel.as_view(), name='label_delete'),
]