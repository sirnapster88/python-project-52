from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse


class UserCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_user = User.objects.create_user(
            username="testuser",
            first_name='test',
            last_name='user',
            password='testpass123'
        )

        self.user_data = {
            'username': 'newuser',
            'first_name': 'new',
            'last_name': 'user',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }

        self.update_data = {
            'username': 'updateuser',
            'first_name': 'update',
            'last_name': 'user',
            'password1': 'testpass123',
            'password2': 'testpass123'
        }

    # CREATE
    def test_uses_correct_template(self):
        response = self.client.get(reverse('users:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/form.html')

    def test_user_create_success(self):
        response = self.client.post(reverse('users:create'), data=self.user_data)  # noqa: E501
        self.assertRedirects(response, reverse('login'))
        created_user = User.objects.get(username='newuser')
        self.assertEqual(created_user.first_name, 'new')
        self.assertEqual(created_user.last_name, 'user')
        self.assertEqual(created_user.username, 'newuser')
        self.assertTrue(created_user.check_password('testpass123'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

    # READ
    def test_user_list_view(self):
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/list.html')

        self.assertIn('users', response.context)

        users = response.context['users']
        self.assertIn(self.test_user, users)

    def test_user_list_show_correct_data(self):
        response = self.client.get(reverse('users:list'))
        self.assertContains(response, 'test')
        self.assertContains(response, 'user')
        self.assertContains(response, 'testuser')

    # UPDATE
    def test_user_update_view_requiers_login(self):
        response = self.client.get(reverse('users:update', args=[self.test_user.id]))  # noqa: E501
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login'))

    def test_user_update_success(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('users:update',
                                            args=[self.test_user.id]),
                                            data=self.update_data)

        self.assertRedirects(response, reverse('users:list'))
        self.test_user.refresh_from_db()

        self.assertEqual(self.test_user.first_name, 'update')
        self.assertEqual(self.test_user.last_name, 'user')
        self.assertEqual(self.test_user.username, 'updateuser')

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

    # DELETE
    def test_user_delete_view_requiers_login(self):
        response = self.client.get(reverse('users:delete', args=[self.test_user.id]))  # noqa: E501
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url.startswith('/login'), True)

    def test_user_delete_success(self):
        self.client.login(username='testuser', password='testpass123')

        user_to_detele = User.objects.create_user(
            username='UserToDelete',
            first_name='User',
            last_name='ToDelete',
            password='passtodelete123'
        )

        user_id = user_to_detele.id

        response = self.client.post(reverse('users:delete', args=[user_id]))

        self.assertRedirects(response, reverse('users:list'))
        self.assertFalse(User.objects.filter(id=user_id).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
# Create your tests here.
