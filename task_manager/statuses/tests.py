from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.tasks.models import Task

from .models import Status


class StatusCRUDViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_user = User.objects.create_user(
            username='testuser',
            first_name='test',
            last_name='user',
            password='testpass123'
        )

        self.status1 = Status.objects.create(name='статус1')
        self.status2 = Status.objects.create(name='статус2')

        self.client.login(username='testuser', password='testpass123')

    # CREATE
    def test_status_create_view_exist_authenticated(self):
        response = self.client.get(reverse('statuses:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/form.html')

    def test_status_create_success(self):
        data = {'name': 'test status'}

        response = self.client.post(reverse('statuses:create'), data)
        self.assertRedirects(response, reverse('statuses:list'))

        self.assertTrue(Status.objects.filter(name='test status').exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

    # READ
    def test_status_list_view_authetnicated(self):
        response = self.client.get(reverse('statuses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/list.html')

    def test_status_list_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('statuses:list'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next={reverse("statuses:list")}')

    # UPDATE
    def test_status_update_view_authenticated(self):
        response = self.client.get(reverse('statuses:update', args=[self.status1.pk]))  # noqa: E501
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/form.html')
        self.assertEqual(response.context['object'], self.status1)

    def test_status_update_successful(self):
        data = {'name': 'updated status'}
        response = self.client.post(reverse('statuses:update', args=[self.status1.pk]), data)  # noqa: E501
        self.assertRedirects(response, reverse('statuses:list'))
        self.status1.refresh_from_db()

        self.assertEqual(self.status1.name, 'updated status')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)

    # DELETE
    def test_status_delete_sucessfully(self):
        response = self.client.post(reverse('statuses:delete', args=[self.status1.pk]))  #noqa: E501

        self.assertRedirects(response, reverse('statuses:list'))
        self.assertFalse(Status.objects.filter(pk=self.status1.pk).exists())

    def test_status_delete_protected_by_task(self):
        Task.objects.create(
            name='Test Task',
            status=self.status1,
            author=self.test_user
        )

        response = self.client.post(reverse('statuses:delete', args=[self.status1.pk]))  #noqa: E501

        self.assertRedirects(response, reverse('statuses:list'))
        self.assertTrue(Status.objects.filter(pk=self.status1.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
# Create your tests here.
