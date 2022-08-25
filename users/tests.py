from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Task


class MyUserTestCase(TestCase):

    fixtures = [
        'test_user.json',
        'test_user2.json',
        'test_task.json',
        'test_status.json'
    ]

    def setUp(self):
        # simulate user logging for auth.system
        user_logged = get_user_model().objects.last()
        self.client.force_login(user_logged)

    def test_log_in_out(self):
        # check response status, template
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/login.html')
        # check login with true login&pass
        user_add = {'first_name': 'test',
                    'last_name': 'test',
                    'username': 'test',
                    'password1': '12345678test',
                    'password2': '12345678test'}
        self.client.post(reverse('user_add'), user_add)
        response = self.client.post(reverse('login'), {'username': 'test', 'password': '12345678test'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        # check login with false login&pass
        response = self.client.post(reverse('login'), {'username': 'test2', 'password': '123458test'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        # check logout
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_users_list(self):
        # check response status, template
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/users_list.html')

    def test_user_add(self):
        # check response status, template
        response = self.client.get(reverse('user_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/user_add.html')
        # check add user
        user_add = {'first_name': 'test',
                    'last_name': 'test',
                    'username': 'test',
                    'password1': '12345678test',
                    'password2': '12345678test'}

        response = self.client.post(reverse('user_add'), user_add)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        # check user added in database
        user = get_user_model().objects.get(username=user_add['username'])
        self.assertEqual(user.username, 'test')
        self.assertEqual(get_user_model().objects.count(), 3)
        # check add user with same username
        response = self.client.post(reverse('user_add'), user_add)
        self.assertFormError(response, 'form', 'username', 'Пользователь с таким именем уже существует.')

    def test_user_update(self):
        # check response status, template
        user = get_user_model().objects.last()
        response = self.client.get(reverse('user_update', args=[user.pk]))
        self.assertEqual(user.username, 'username_test2')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/user_update.html')
        # check update user
        user_update_info = {
            'first_name': 'first_name_test1',
            'last_name': 'last_name_test1',
            'username': 'username_test1',
            'password1': 'qwerty123456ZZ',
            'password2': 'qwerty123456ZZ',
        }
        response = self.client.post(reverse('user_update', args=[user.pk]), user_update_info)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        # check user updated in database
        user_updated = get_user_model().objects.last()
        self.assertEqual(user_updated.first_name, 'first_name_test1')
        self.assertTrue(user_updated.check_password('qwerty123456ZZ'))

    def test_user_delete(self):
        # check response status, template
        user = get_user_model().objects.last()
        response = self.client.get(reverse('user_delete', args=[user.pk]))
        self.assertEqual(user.username, 'username_test2')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/user_delete.html')
        # check delete user
        response = self.client.post(reverse('user_delete', args=[user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        # check user deleted from database
        self.assertEqual(get_user_model().objects.count(), 1)
        # check delete one user by another user
        user_add = {'first_name': 'test',
                    'last_name': 'test',
                    'username': 'test',
                    'password1': '12345678test',
                    'password2': '12345678test'}
        self.client.post(reverse('user_add'), user_add)
        user2 = get_user_model().objects.last()
        self.assertEqual(user2.username, 'test')
        response = self.client.post(reverse('user_delete', args=[user2.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        # check user not deleted from database
        self.assertEqual(get_user_model().objects.count(), 2)

    def test_user_linked_with_task_delete(self):
        # check response status, template
        user = get_user_model().objects.first()
        self.client.force_login(user)
        response = self.client.post(reverse('user_delete', args=[user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        # check user not deleted from database, cause of protect
        self.assertEqual(get_user_model().objects.count(), 2)
