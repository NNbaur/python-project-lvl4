from django.db import models
from statuses.models import Status
from users.models import MyUser


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True, null=False, blank=False, verbose_name='Имя')
    description = models.TextField(blank=True, verbose_name='Описание')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name='Статус')
    author = models.ForeignKey(MyUser, on_delete=models.PROTECT, verbose_name='Автор', related_name='authors')
    executor = models.ForeignKey(MyUser, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Исполнитель', related_name='executors')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'