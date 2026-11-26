
from django.db import models
from django.urls import reverse


class Departamento(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre'
    )

    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )

    fecha_creacion = models.DateField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )

    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse(
            'personal:departamento_detalle',
            kwargs={'pk': self.pk}
        )

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        ordering = ['nombre']
