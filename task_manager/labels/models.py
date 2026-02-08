from django.db import models
from django.utils.translation import gettext_lazy

class Label(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name=gettext_lazy('Имя'))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
# Create your models here.
