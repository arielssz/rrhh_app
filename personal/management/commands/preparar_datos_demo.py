from datetime import date
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth.models import Group, User
from personal.models import Departamento, Cargo, Capacitacion, Empleado


class Command(BaseCommand):
    help = 'Prepara usuarios y cinco registros de demostración por cada modelo.'

    def handle(self, *args, **options):
        call_command('configurar_roles')
        grupo_admin = Group.objects.get(name='Administrador')
        grupo_consultor = Group.objects.get(name='Consultor')

        admin, creado = User.objects.get_or_create(
            username='admin_demo',
            defaults={'email': 'admin_demo@example.com', 'is_staff': True, 'is_superuser': True},
        )
        if creado:
            admin.set_password('AdminDemo123!')
            admin.save()
        admin.groups.add(grupo_admin)

        administrador, creado = User.objects.get_or_create(
            username='administrador_demo',
            defaults={'email': 'administrador_demo@example.com', 'is_staff': True},
        )
        if creado:
            administrador.set_password('AdministradorDemo123!')
            administrador.save()
        administrador.groups.add(grupo_admin)

        consultor, creado = User.objects.get_or_create(
            username='consultor_demo',
            defaults={'email': 'consultor_demo@example.com'},
        )
        if creado:
            consultor.set_password('ConsultorDemo123!')
            consultor.save()
        consultor.groups.add(grupo_consultor)

        departamentos = []
        for nombre in ['Recursos Humanos', 'Finanzas', 'Tecnología', 'Operaciones', 'Ventas']:
            obj, _ = Departamento.objects.get_or_create(nombre=nombre, defaults={'descripcion': f'Departamento de {nombre}'})
            departamentos.append(obj)

        cargos = []
        for nombre, salario in [('Analista', '800.00'), ('Asistente', '600.00'), ('Coordinador', '1200.00'), ('Desarrollador', '1500.00'), ('Supervisor', '1100.00')]:
            obj, _ = Cargo.objects.get_or_create(nombre=nombre, defaults={'salario_base': salario, 'descripcion': f'Cargo de {nombre}'})
            cargos.append(obj)

        capacitaciones = []
        for i, nombre in enumerate(['Inducción institucional', 'Seguridad laboral', 'Excel intermedio', 'Protección de datos', 'Atención al cliente']):
            obj, _ = Capacitacion.objects.get_or_create(
                nombre=nombre,
                defaults={'modalidad': 'PRESENCIAL' if i % 2 == 0 else 'VIRTUAL',
                          'fecha_inicio': date(2026, 1, 5 + i), 'fecha_fin': date(2026, 1, 5 + i),
                          'duracion_horas': 8 + i},
            )
            capacitaciones.append(obj)

        nombres = [('Ana', 'Pérez'), ('Luis', 'Gómez'), ('María', 'López'), ('Carlos', 'Mora'), ('Sofía', 'Vera')]
        for i, (nombre, apellido) in enumerate(nombres):
            empleado, _ = Empleado.objects.get_or_create(
                cedula=f'179000000{i+1}',
                defaults={'nombres': nombre, 'apellidos': apellido,
                          'email': f'empleado{i+1}@demo.local',
                          'fecha_contratacion': date(2026, 1, 1),
                          'departamento': departamentos[i], 'cargo': cargos[i],
                          'creado_por': consultor},
            )
            empleado.capacitaciones.add(capacitaciones[i])

        self.stdout.write(self.style.SUCCESS(
            'Datos demo listos: 5 departamentos, 5 cargos, 5 capacitaciones y 5 empleados. '
            'Usuarios: admin_demo / AdminDemo123!, administrador_demo / AdministradorDemo123! y consultor_demo / ConsultorDemo123!'
        ))
