from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Status


class StatusTestCase(TestCase):

    fixtures = [
        'test_user.json',
        'test_status.json',
        'test_status2.json',
        'test_task.json'
    ]

    def setUp(self):
        # simulate user logging for auth.system
        user_logged = get_user_model().objects.last()
        self.client.force_login(user_logged)

    def test_statuses_list(self):
        # check response status, template
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/statuses_list.html')

    def test_status_add(self):
        # check response status, template
        response = self.client.get(reverse('status_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/status_add.html')
        # check add status
        status_add = {'name': 'test'}
        response = self.client.post(reverse('status_add'), status_add)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        # check status added in database
        status = Status.objects.get(name=status_add['name'])
        self.assertEqual(status.name, 'test')
        self.assertEqual(Status.objects.count(), 3)
        # check add status with same name
        response = self.client.post(reverse('status_add'), status_add)
        self.assertFormError(response, 'form', 'name', 'Статус с таким именем уже существует!')

    def test_status_update(self):
        # check response status, template
        status = Status.objects.last()
        response = self.client.get(reverse('status_update', args=[status.pk]))
        self.assertEqual(status.name, 'status_test2')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/status_update.html')
        # check update status
        status_update_info = {
            'name': 'status_test1'}
        response = self.client.post(reverse('status_update', args=[status.pk]), status_update_info)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        # check status updated in database
        status_updated = Status.objects.last()
        self.assertEqual(status_updated.name, 'status_test1')

    def test_status_delete(self):
        # check response status, template
        status = Status.objects.last()
        response = self.client.get(reverse('status_delete', args=[status.pk]))
        self.assertEqual(status.name, 'status_test2')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/status_delete.html')
        # check delete status
        response = self.client.post(reverse('status_delete', args=[status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        # check status deleted from database
        self.assertEqual(Status.objects.count(), 1)

    def test_status_linked_with_task_delete(self):
        # check response status, template
        status = Status.objects.first()
        response = self.client.post(reverse('status_delete', args=[status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('status_list'))
        # check status not deleted from database, cause of protect
        self.assertEqual(Status.objects.count(), 2)
