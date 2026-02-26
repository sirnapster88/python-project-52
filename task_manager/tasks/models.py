from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy
from task_manager.statuses.models import Status


User = get_user_model()

class Task(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    description = models.TextField(verbose_name="Описание")
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name='Статус'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='authored_task',
        verbose_name='Автор'
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='assigned_tasks',
        null=True,
        blank=True,
        verbose_name='Исполнитель'   
    )
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField('labels.Label',
                                    verbose_name=gettext_lazy('Метки'))
    
    def __str__(self):
        return self.name
# Create your models here.
