from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Label


class LabelTestCase(TestCase):

    fixtures = [
        'test_user.json',
        'test_label.json',
        'test_label2.json',
        'test_task.json',
        'test_status.json',
        'test_label.json',
        'test_task_label.json'
    ]

    def setUp(self):
        # simulate user logging for auth.system
        user_logged = get_user_model().objects.last()
        self.client.force_login(user_logged)

    def test_label_list(self):
        # check response status, template
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/label_list.html')

    def test_label_add(self):
        # check response status, template
        response = self.client.get(reverse('label_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/label_add.html')
        # check add label
        label_add = {'name': 'test_label1'}
        response = self.client.post(reverse('label_add'), label_add)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        # check label added in database
        label = Label.objects.get(name=label_add['name'])
        self.assertEqual(label.name, 'test_label1')
        self.assertEqual(Label.objects.count(), 3)
        # check add label with same name
        response = self.client.post(reverse('label_add'), label_add)
        self.assertFormError(response, 'form', 'name', 'Метка с таким именем уже существует!')

    def test_label_update(self):
        # check response status, template
        label = Label.objects.last()
        response = self.client.get(reverse('label_update', args=[label.pk]))
        self.assertEqual(label.name, 'label_test2')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/label_update.html')
        # check update label
        label_update_info = {
            'name': 'label_test1'}
        response = self.client.post(reverse('label_update', args=[label.pk]), label_update_info)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        # check status updated in database
        label_updated = Label.objects.last()
        self.assertEqual(label_updated.name, 'label_test1')

    def test_label_delete(self):
        # check response status, template
        label = Label.objects.last()
        response = self.client.get(reverse('label_delete', args=[label.pk]))
        self.assertEqual(label.name, 'label_test2')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/label_delete.html')
        # check delete label
        response = self.client.post(reverse('label_delete', args=[label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        # check label deleted from database
        self.assertEqual(Label.objects.count(), 1)

    def test_label_linked_with_task_delete(self):
        # check response status, template
        label = Label.objects.first()
        response = self.client.post(reverse('label_delete', args=[label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('label_list'))
        # check label not deleted from database, cause of protect
        self.assertEqual(Label.objects.count(), 2)