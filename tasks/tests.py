from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import *


class TaskTestCase(TestCase):

    fixtures = ['test_user.json', 'test_status.json', 'test_task.json']

    def setUp(self):
        # simulate user logging for auth.system
        user_logged = get_user_model().objects.first()
        self.client.force_login(user_logged)

    def test_task_list(self):
        # check response status, template
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/task_list.html')

    def test_task_view(self):
        # check response status, template
        task = Task.objects.first()
        response = self.client.get(reverse('task_view', args=[task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/task_view.html')

    def test_task_add(self):
        # check response status, template
        response = self.client.get(reverse('task_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/task_add.html')
        # check add task
        status = Status.objects.first()
        user = get_user_model().objects.first()
        task_add = {
            'name': 'test_task1',
            'description': 'desc_test1',
            'executor': user.pk,
            'status': status.pk
        }
        response = self.client.post(reverse('task_add'), task_add)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        # check task added in database and foreignkey is correct
        task = Task.objects.last()
        self.assertEqual(task.name, 'test_task1')
        self.assertEqual(task.description, 'desc_test1')
        self.assertEqual(task.status.name, 'status_test')
        self.assertEqual(task.executor.username, 'username_test')
        self.assertEqual(task.author.username, 'username_test')
        self.assertEqual(Task.objects.count(), 2)
        # check add task with same name
        response = self.client.post(reverse('task_add'), task_add)
        self.assertFormError(response, 'form', 'name', 'Задача с таким именем уже существует!')

    def test_task_update(self):
        # check response status, template
        task = Task.objects.first()
        response = self.client.get(reverse('task_update', args=[task.pk]))
        self.assertEqual(task.name, 'task_test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/task_update.html')
        # check update task
        status = Status.objects.first()
        user = get_user_model().objects.first()

        task_update_info = {
            'name': 'new_task1',
            'description': 'new_desc1',
            'executor': user.pk,
            'status': status.pk
        }
        response = self.client.post(reverse('task_update', args=[task.pk]), task_update_info)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        # check task updated in database
        task_updated = Task.objects.first()
        self.assertEqual(task_updated.name, 'new_task1')

    def test_task_delete_by_author(self):
        # check response status, template
        task = Task.objects.first()
        response = self.client.get(reverse('task_delete', args=[task.pk]))
        self.assertEqual(task.name, 'task_test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/task_delete.html')
        # check delete task by author
        response = self.client.post(reverse('task_delete', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        # check task deleted from database
        self.assertEqual(Task.objects.count(), 0)

    def test_task_delete_by_not_author(self):
        # check delete task by not author
        user_not_author = get_user_model().objects.create(
            password="pass_test",
            username="not_author",
            first_name="first_name_test2",
            last_name="last_name_test2",
        )
        self.client.force_login(user_not_author)
        task = Task.objects.first()
        response = self.client.get(reverse('task_delete', args=[task.pk]))
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('task_delete', args=[task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task_list'))
        self.assertEqual(Task.objects.count(), 1)