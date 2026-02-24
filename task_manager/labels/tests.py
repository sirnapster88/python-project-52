from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from .models import Label
from .forms import LabelForm
from task_manager.tasks.models import Task

class LabelCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.test_user = User.objects.create_user(
            username="testuser",
            password="testuser123"
        )

        self.label1 = Label.objects.create(name='Метка 1')
        self.label2 = Label.objects.create(name='Метка 2')

        self.client.login(username='testuser', password='testuser123')

    #CREATE
    def test_label_create_view_authenticated(self):
        response = self.client.get(reverse('labels:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/form.html')
        self.assertEqual(response.context['title'], 'Создать метку')
        self.assertEqual(response.context['form_title'], 'Создать метку')
        self.assertEqual(response.context['submit_button'], 'Создать')

    def test_label_create_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('labels:create'))
        self.assertRedirects(response, f'/login/?next={reverse("labels:create")}')

    def test_create_label_success(self):
        data = {'name': 'Новая метка'}
        response = self.client.post(reverse('labels:create'), data)

        self.assertRedirects(response, reverse('labels:list'))
        self.assertTrue(Label.objects.filter(name='Новая метка').exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Метка успешно создана')

    def test_label_create_duplicate_name(self):
        data = {'name': 'Метка 1'}
        response = self.client.post(reverse('labels:create'), data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('name', response.context['form'].errorss)

    #READ
    def test_label_list_view_authenticated(self):
        response = self.client.get(reverse('labels:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/list.html')
        self.assertEqual(response.context['title'], 'Метки')
        self.assertEqual(len(response.context['labels']), 2)

    def test_label_list_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('labels:list'))
        self.assertRedirects(response, f'/login/?next={reverse("labels:list")}')

    
    def test_label_list_diaplays_correct_data(self):
        response = self.client.get(reverse('labels:list'))
        self.assertContains(response, 'Метка 1')
        self.assertContains(response, 'Метка 2')

    #UPDATE
    def test_label_update_view_authenticated(self):
        response = self.client.get(reverse("labels:update"), args=[self.label1.pk])
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/form.html')
        self.assertEqual(response.context['title'], 'Изменение метки')
        self.assertEqual(response.context['form_title'], 'Изменение метки')
        self.assertEqual(response.context['submit_button'], 'Изменить')
        self.assertEqual(response.context['form'].instance, self.label1)

    def test_label_update_success(self):
        data = {'name': 'Обновленная метка'}
        response = self.client.post(reverse('labels:update', args=[self.label1.pk]), data)

        self.assertRedirects(response, reverse('labels:list'))
        self.label1.refresh_from_db()
        self.assertEqual(self.label1.name, 'Обновленная метка')

    def test_label_update_duplicate_name(self):
        data = {'name': 'Метка 2'}
        response = self.client.post(reverse('labels:update', args=[self.label1.pk]), data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('name', response.context['form'].errors)

    #DELETE
    def test_label_delete_authenticated(self):
        response = self.client.get(reverse('labels:delete', args=[self.label1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/delete.html')
        self.assertEqual(response.context['title'], 'Удаление метки')
        self.assertEqual(response.context['form_title'], 'Удаление метки')
        self.assertEqual(response.context['submit_button'], 'Да, удалить')

    def test_label_delete_succes(self):
        response = self.client.post(reverse('labels:delete', args=[self.label1.pk]))

        self.assertRedirects(response, reverse('labels:list'))
        self.assertFalse(Label.objects.filter(pk=self.label1.pk).exists())

    def test_label_delete_protected_by_task(self):
        task = Task.objects.create(
            name='Тестовая задача',
            author=self.test_user,
            status_id=1
        )
        
        task.labels.add(self.label1)
        response = self.client.post(reverse('labels:delete', args=[self.label1.pk]))

        self.assertRedirects(response, reverse('labels:list'))
        self.assertTrue(Label.objects.filter(pk=self.label1.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        
    # Create your tests here.
