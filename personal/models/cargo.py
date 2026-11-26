
from django.db import models
from django.urls import reverse


class Cargo(models.Model):

    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre del cargo'
    )

    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )

    salario_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Salario base'
    )

    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )

    fecha_creacion = models.DateField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse(
            'personal:cargo_detalle',
            kwargs={'pk': self.pk}
        )

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['nombre']
