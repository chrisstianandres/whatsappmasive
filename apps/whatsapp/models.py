from datetime import datetime

from django.db import models
from django.forms import model_to_dict


class Mensaje(models.Model):
    mensaje = models.CharField(max_length=500)
    numero_veces = models.IntegerField(default=1)

    def __str__(self):
        return '{} '.format(self.mensaje)

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        db_table = 'mensaje'
        verbose_name = 'mensaje'
        verbose_name_plural = 'mensajes'
        ordering = ['-mensaje']