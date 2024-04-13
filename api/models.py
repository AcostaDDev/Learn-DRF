from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    complete = models.BooleanField(default=False, verbose_name='Completo')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title