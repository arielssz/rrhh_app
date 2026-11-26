
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Empleado(models.Model):

    class Estado(models.TextChoices):
        ACTIVO = 'ACTIVO', 'Activo'
        INACTIVO = 'INACTIVO', 'Inactivo'
        VACACIONES = 'VACACIONES', 'Vacaciones'

    cedula = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Cédula'
    )

    nombres = models.CharField(
        max_length=100,
        verbose_name='Nombres'
    )

    apellidos = models.CharField(
        max_length=100,
        verbose_name='Apellidos'
    )

    email = models.EmailField(
        unique=True,
        verbose_name='Correo electrónico'
    )

    telefono = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Teléfono'
    )

    fecha_nacimiento = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de nacimiento'
    )

    fecha_contratacion = models.DateField(
        verbose_name='Fecha de contratación'
    )

    estado = models.CharField(
        max_length=15,
        choices=Estado.choices,
        default=Estado.ACTIVO,
        verbose_name='Estado'
    )

    departamento = models.ForeignKey(
        'personal.Departamento',
        on_delete=models.PROTECT,
        related_name='empleados',
        verbose_name='Departamento'
    )

    cargo = models.ForeignKey(
        'personal.Cargo',
        on_delete=models.PROTECT,
        related_name='empleados',
        verbose_name='Cargo'
    )

    capacitaciones = models.ManyToManyField(
        'personal.Capacitacion',
        blank=True,
        related_name='empleados',
        verbose_name='Capacitaciones'
    )

    creado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='empleados_creados',
        verbose_name='Creado por'
    )

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

    def get_absolute_url(self):
        return reverse(
            'personal:empleado_detalle',
            kwargs={'pk': self.pk}
        )

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['apellidos', 'nombres']
