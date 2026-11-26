
from django.db import models
from django.urls import reverse


class Capacitacion(models.Model):

    class Modalidad(models.TextChoices):
        PRESENCIAL = 'PRESENCIAL', 'Presencial'
        VIRTUAL = 'VIRTUAL', 'Virtual'
        HIBRIDA = 'HIBRIDA', 'Híbrida'

    nombre = models.CharField(
        max_length=150,
        verbose_name='Nombre de la capacitación'
    )

    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )

    modalidad = models.CharField(
        max_length=15,
        choices=Modalidad.choices,
        default=Modalidad.PRESENCIAL,
        verbose_name='Modalidad'
    )

    fecha_inicio = models.DateField(
        verbose_name='Fecha de inicio'
    )

    fecha_fin = models.DateField(
        verbose_name='Fecha de finalización'
    )

    duracion_horas = models.PositiveIntegerField(
        verbose_name='Duración en horas'
    )

    activa = models.BooleanField(
        default=True,
        verbose_name='Activa'
    )

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse(
            'personal:capacitacion_detalle',
            kwargs={'pk': self.pk}
        )

    class Meta:
        verbose_name = 'Capacitación'
        verbose_name_plural = 'Capacitaciones'
        ordering = ['-fecha_inicio']
