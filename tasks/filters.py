from .models import Task
import django_filters
from django import forms

class TaskFilter(django_filters.FilterSet):
    self_task = django_filters.BooleanFilter(method='user_is_creator',
                                             widget=forms.CheckboxInput)

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_task']
        filter_overrides = {
            django_filters.BooleanFilter: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }

    def user_is_creator(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset