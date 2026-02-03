from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from .models import Status
from .forms import StatusForm 


class StatusCRUDViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_user = User.objects.create(
            username = 'testuser',
            first_name = 'test',
            last_name = 'user',
            password = 'testpass123'
        )

        self.status1 = Status.objects.create(name='статус1')
        self.status2 = Status.objects.create(name='статус2')

        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
    
    
    #CREATE
    def test_status_create_view_exist_authenticated(self):
        response = self.client.get(reverse('statuses:create'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'statuses/create.html')
    
    def test_status_create_success(self):
        data = {'name': 'test status'}

        response = self.client.post(reverse('statuses:create'), data)
        self.assertRedirects(response, reverse('statuses:list'))

        self.assertTrue(Status.objects.filter('тестовый статус'.exists()))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
    
    #READ
    def test_status_list_view_authetnicated(self):
        response = self.client.get(reverse('statuses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/list.html')

    def test_status_list_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('statuses:list'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/login/?next={reverse('statuses:list')}')

    #UPDATE
    def test_status_update_view_authenticated(self):
        response = self.client.get(reverse('statuses:update', args=[self.status1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'statuses/update.html')
        self.assertEqual(response.content['object'], self.status1)

    def test_status_update_successfuly(self):
        data = {'name': 'updated status'}
        response = self.client.post(reverse('statuses:update', args=[self.status1.pk]), data)
        self.assertRedirects(response, reverse('statuses:list'))
        self.status1.refresh_from_db()

        self.assertEqual(self.status1.name, 'updated status')

    #DELETE
    def test_status_delete_sucessfully(self):
        response = self.client.post(reverse('statuses:delete'), args=[self.status1.pk])

        self.assertRedirects(response, reverse('statuses:list'))
        self.assertFalse(Status.objects.filter(pk=self.status1.pk).exists())
# Create your tests here.
