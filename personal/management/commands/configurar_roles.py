from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from personal.models import Departamento, Cargo, Empleado, Capacitacion


class Command(BaseCommand):
    help = 'Crea o actualiza los grupos Administrador y Consultor con sus permisos.'

    def handle(self, *args, **options):
        modelos = [Departamento, Cargo, Empleado, Capacitacion]
        permisos_por_modelo = {}

        for modelo in modelos:
            content_type = ContentType.objects.get_for_model(modelo)
            permisos_por_modelo[modelo.__name__.lower()] = list(
                Permission.objects.filter(content_type=content_type)
            )

        administrador, _ = Group.objects.get_or_create(name='Administrador')
        todos = [permiso for permisos in permisos_por_modelo.values() for permiso in permisos]
        administrador.permissions.set(todos)

        consultor, _ = Group.objects.get_or_create(name='Consultor')
        permitidos = []
        for nombre_modelo, permisos in permisos_por_modelo.items():
            permitidos.extend(
                permiso for permiso in permisos
                if permiso.codename.startswith('view_')
                or permiso.codename.startswith('add_')
                or (nombre_modelo == 'empleado' and permiso.codename == 'change_empleado')
            )
        consultor.permissions.set(permitidos)

        self.stdout.write(self.style.SUCCESS(
            'Roles configurados: Administrador (CRUD completo) y Consultor '
            '(ver/crear en todos los módulos y editar únicamente empleados propios, '
            'controlado por la vista).'
        ))
