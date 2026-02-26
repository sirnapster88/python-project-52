from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

class TaskCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()

        self.author = User.objects.create_user(
            username='author',
            password='author123'
        )

        self.executor = User.objects.create_user(
            username='executor',
            password='executor123'
        )

        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otheruser123'
        )

        self.status = Status.objects.create(name='Тестовый статус')

        self.label1 = Label.objects.create(name='Метка 1')
        self.label2 = Label.objects.create(name='Метка 2')

        self.task = Task.objects.create(
            name='Тестовая задача',
            description='Описание тестовой задачи',
            status=self.status,
            author=self.author,
            executor=self.executor
        )

        self.task.labels.add(self.label1)

        self.client.login(username='author', password='author123')

    #CREATE
    def test_task_create_view_authenticated(self):
        response = self.client.get(reverse('tasks:create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/form.html')
        self.assertEqual(response.context['title'], 'Создать задачу')
        self.assertEqual(response.context['form_title'], 'Создать задачу')
        self.assertEqual(response.context['submit_button'], 'Создать')

    def test_task_create_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('tasks:create'))
        self.assertRedirects(response, f'/login/?next={reverse("tasks:create")}')

    def test_task_create_success(self):
        data = {
            'name': 'Новая Тестовая задача',
            'description': 'Описание тестовой задачи',
            'status': self.status.pk,
            'executor': self.executor.pk,
            'labels': [self.label1.pk, self.label2.pk]
        }        

        response = self.client.post(reverse('tasks:create'), data)

        self.assertRedirects(response, reverse('tasks:list'))
        task = Task.objects.get(name='Новая Тестовая задача')
        self.assertEqual(task.description, 'Описание тестовой задачи')
        self.assertEqual(task.author, self.author)
        self.assertEqual(task.executor, self.executor)
        self.assertEqual(task.status, self.status)
        self.assertEqual(task.labels.count(), 2)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Задача успешно создана')


    #READ
    def test_tasks_list_view_authenticated(self):
        response = self.client.get(reverse('tasks:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/list.html')
        self.assertEqual(response.context['title'], 'Задачи')
        self.assertIn('filter_form', response.context)
        filter_form = response.context['filter_form']
        self.assertIn('executor', filter_form.fields)
        self.assertEqual(filter_form.fields['executor'].label, 'Исполнитель')
        self.assertContains(response, 'Исполнитель')
        self.assertContains(response, 'name="executor"')

    def test_tasks_filter_by_status(self):
        new_status = Status.objects.create(name='Новый статус')
        Task.objects.create(
            name='Задача 2',
            status=new_status,
            author=self.author
        )

        response = self.client.get(reverse('tasks:list'), {'status': new_status.pk})
        self.assertContains(response, 'Задача 2')
        self.assertNotContains(response, 'Тестовая задача')

    
    def test_tasks_filter_by_executor(self):
        Task.objects.create(
            name='Задача 2',
            status=self.status,
            author=self.author,
            executor=self.other_user
        )

        response = self.client.get(reverse('tasks:list'), {'executor': self.other_user.pk})
        self.assertContains(response, 'Задача 2')
        self.assertNotContains(response, 'Тестовая задача')

    
    def test_tasks_filter_by_label(self):
        task2 = Task.objects.create(
            name='Задача 2',
            status=self.status,
            author=self.author
        )
        task2.labels.add(self.label2)

        response = self.client.get(reverse('tasks:list'), {'label': self.label2.id})
        self.assertContains(response, 'Задача 2')
        self.assertNotContains(response, 'Тестовая задача')
    
    def test_tasks_filter_by_my_tasks(self):
        Task.objects.create(
            name='Задача другого пользователя',
            status=self.status,
            author=self.other_user
        )

        response = self.client.get(reverse('tasks:list'), {'my_task': 'on'})
        self.assertContains(response, 'Тестовая задача')
        self.assertNotContains(response, 'Задача другого пользователя')
    
    #DETAIL
    def test_tasks_detail_view_authenticated(self):
        response = self.client.get(reverse('tasks:detail_view', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/detail_view.html')
        self.assertEqual(response.context['task'], self.task)

    #UPDATE
    def test_task_update_view_authenticated(self):
        response = self.client.get(reverse('tasks:update', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/form.html')
        self.assertEqual(response.context['title'], 'Изменение задачи')
        self.assertEqual(response.context['form_title'], 'Изменение задачи')
        self.assertEqual(response.context['submit_button'], 'Изменить')

    def test_task_update_success(self):
        data = {
            'name': 'Обновленная задача',
            'description': 'Описание обновленной задачи',
            'status': self.status.pk,
            'executor': self.other_user.pk,
            'labels': [self.label2.pk]
        }
        response = self.client.post(reverse('tasks:update', args=[self.task.pk]), data)
        self.assertRedirects(response, reverse('tasks:list'))
        self.task.refresh_from_db()

        self.assertEqual(self.task.name, 'Обновленная задача')
        self.assertEqual(self.task.description, 'Описание обновленной задачи')
        self.assertEqual(self.task.executor, self.other_user)
        self.assertEqual(self.task.labels.count(), 1)
        self.assertEqual(self.task.labels.first(), self.label2)

    #DELETE
    def test_task_delete_authenticated(self):
        response = self.client.get(reverse('tasks:delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/delete.html')
        self.assertEqual(response.context['title'], 'Удаление задачи')
        self.assertEqual(response.context['delete_title'], 'Удаление задачи')
        self.assertEqual(response.context['submit_button'], 'Да, удалить')

    def test_task_delete_by_author_success(self):
        response = self.client.post(reverse('tasks:delete', args=[self.task.pk]))

        self.assertRedirects(response, reverse('tasks:list'))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
    
    def test_task_delete_by_non_author(self):
        self.client.logout()
        self.client.login(username='otheruser', password='otheruser123')

        response = self.client.post(reverse('tasks:delete', args=[self.task.pk]))

        self.assertRedirects(response, reverse('tasks:list'))
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
# Create your tests here.


