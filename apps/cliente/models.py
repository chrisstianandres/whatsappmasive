from datetime import datetime

from django.db import models
from django.forms import model_to_dict

from whatsappmasive.settings import MEDIA_URL

SEXO = (
    (1, 'Masculino'),
    (0, 'Femenino'),
)


class Cliente(models.Model):
    nombres = models.CharField(max_length=50)
    telefono = models.CharField(max_length=13, unique=True)
    fecha = models.DateField(default=datetime.now)

    def __str__(self):
        return '{} '.format(self.nombres)

    def toJSON(self):
        item = model_to_dict(self)
        item['fecha'] = self.fecha.strftime('%d/%m/%Y')
        return item

    class Meta:
        db_table = 'cliente'
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'
        ordering = ['-nombres']


class Filexls(models.Model):
    archivo = models.FileField(upload_to='files/%Y/%m/%d', null=True, blank=True)

    # def __str__(self):
    #     return '{} '.format(self.archivo.path)
    #
    # def get_file(self):
    #     if self.archivo:
    #         return '{}{}'.format(MEDIA_URL, self.archivo)

    def toJSON(self):
        item = model_to_dict(self)
        # item['archivo'] = self.get_file()
        return item

    class Meta:
        db_table = 'archivo'
        verbose_name = 'archivo'
        verbose_name_plural = 'archivos'
        ordering = ['-archivo']


