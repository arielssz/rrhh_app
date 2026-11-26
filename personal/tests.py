from datetime import date
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

from personal.models import Departamento, Cargo, Empleado, Capacitacion
from personal.forms import CapacitacionForm, EmpleadoForm


class PermisosRolesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.consultor = User.objects.create_user(username='consultor_test', password='ClaveSegura123!')
        cls.otro_usuario = User.objects.create_user(username='otro_test', password='ClaveSegura123!')
        cls.admin = User.objects.create_superuser(username='admin_test', email='admin@test.local', password='ClaveSegura123!')

        grupo, _ = Group.objects.get_or_create(name='Consultor')
        permisos = []
        for modelo in (Departamento, Cargo, Empleado, Capacitacion):
            ct = ContentType.objects.get_for_model(modelo)
            permisos.extend(Permission.objects.filter(content_type=ct, codename__startswith='view_'))
            permisos.extend(Permission.objects.filter(content_type=ct, codename__startswith='add_'))
        ct_empleado = ContentType.objects.get_for_model(Empleado)
        permisos.extend(Permission.objects.filter(content_type=ct_empleado, codename='change_empleado'))
        grupo.permissions.set(permisos)
        cls.consultor.groups.add(grupo)

        cls.departamento = Departamento.objects.create(nombre='Administración')
        cls.cargo = Cargo.objects.create(nombre='Analista', salario_base='800.00')
        cls.capacitacion = Capacitacion.objects.create(
            nombre='Inducción', modalidad='PRESENCIAL', fecha_inicio=date(2026, 1, 10),
            fecha_fin=date(2026, 1, 10), duracion_horas=8,
        )
        cls.empleado_propio = Empleado.objects.create(
            cedula='1700000001', nombres='Ana', apellidos='Prueba', email='ana@test.local',
            fecha_contratacion=date(2026, 1, 1), departamento=cls.departamento,
            cargo=cls.cargo, creado_por=cls.consultor,
        )
        cls.empleado_ajeno = Empleado.objects.create(
            cedula='1700000002', nombres='Luis', apellidos='Prueba', email='luis@test.local',
            fecha_contratacion=date(2026, 1, 1), departamento=cls.departamento,
            cargo=cls.cargo, creado_por=cls.otro_usuario,
        )

    def iniciar_consultor(self):
        self.client.force_login(self.consultor)

    def test_consultor_ve_listados_pero_no_acciones_restringidas(self):
        self.iniciar_consultor()
        casos = [
            ('personal:departamento_lista', 'Editar', 'Eliminar'),
            ('personal:cargo_lista', 'Editar', 'Eliminar'),
            ('personal:capacitacion_lista', 'Editar', 'Eliminar'),
        ]
        for nombre_url, texto_editar, texto_eliminar in casos:
            response = self.client.get(reverse(nombre_url))
            self.assertEqual(response.status_code, 200)
            self.assertNotContains(response, texto_editar)
            self.assertNotContains(response, texto_eliminar)

    def test_consultor_no_puede_editar_ni_eliminar_departamento(self):
        self.iniciar_consultor()
        self.assertEqual(self.client.get(reverse('personal:departamento_editar', args=[self.departamento.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse('personal:departamento_eliminar', args=[self.departamento.pk])).status_code, 403)

    def test_consultor_no_puede_editar_ni_eliminar_cargo(self):
        self.iniciar_consultor()
        self.assertEqual(self.client.get(reverse('personal:cargo_editar', args=[self.cargo.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse('personal:cargo_eliminar', args=[self.cargo.pk])).status_code, 403)

    def test_consultor_no_puede_editar_ni_eliminar_capacitacion(self):
        self.iniciar_consultor()
        self.assertEqual(self.client.get(reverse('personal:capacitacion_editar', args=[self.capacitacion.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse('personal:capacitacion_eliminar', args=[self.capacitacion.pk])).status_code, 403)

    def test_consultor_edita_solo_empleados_propios(self):
        self.iniciar_consultor()
        self.assertEqual(self.client.get(reverse('personal:empleado_editar', args=[self.empleado_propio.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse('personal:empleado_editar', args=[self.empleado_ajeno.pk])).status_code, 403)
        self.assertEqual(self.client.get(reverse('personal:empleado_eliminar', args=[self.empleado_propio.pk])).status_code, 403)

    def test_consultor_puede_crear_en_los_modulos(self):
        self.iniciar_consultor()
        for nombre_url in ('personal:departamento_crear', 'personal:cargo_crear', 'personal:empleado_crear', 'personal:capacitacion_crear'):
            self.assertEqual(self.client.get(reverse(nombre_url)).status_code, 200)

    def test_administrador_puede_acceder_a_edicion_y_eliminacion(self):
        self.client.force_login(self.admin)
        rutas = [
            ('personal:departamento_editar', self.departamento.pk),
            ('personal:cargo_editar', self.cargo.pk),
            ('personal:capacitacion_editar', self.capacitacion.pk),
            ('personal:empleado_editar', self.empleado_ajeno.pk),
        ]
        for nombre_url, pk in rutas:
            self.assertEqual(self.client.get(reverse(nombre_url, args=[pk])).status_code, 200)

    def test_registro_crea_usuario_en_grupo_consultor(self):
        response = self.client.post(reverse('registro'), {
            'username': 'nuevo_usuario',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'email': 'nuevo@example.com',
            'password1': 'ClaveFuerte2026!Seguro',
            'password2': 'ClaveFuerte2026!Seguro',
        })
        self.assertRedirects(response, reverse('login'))
        nuevo = User.objects.get(username='nuevo_usuario')
        self.assertTrue(nuevo.groups.filter(name='Consultor').exists())

    def test_logout_solo_acepta_post(self):
        self.iniciar_consultor()
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
        self.assertEqual(self.client.post(reverse('logout')).status_code, 302)

    def test_vista_protegida_envia_anonimo_al_login(self):
        response = self.client.get(reverse('personal:empleado_lista'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_validacion_propia_de_capacitacion(self):
        form = CapacitacionForm(data={
            'nombre': 'Fechas incorrectas', 'descripcion': '', 'modalidad': 'PRESENCIAL',
            'fecha_inicio': '2026-02-10', 'fecha_fin': '2026-02-09',
            'duracion_horas': 8, 'activa': True,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('fecha_fin', form.errors)

    def test_validacion_propia_de_cedula(self):
        form = EmpleadoForm(data={
            'cedula': '123', 'nombres': 'Prueba', 'apellidos': 'Usuario',
            'email': 'prueba@example.com', 'telefono': '', 'fecha_nacimiento': '',
            'fecha_contratacion': '2026-01-01', 'estado': 'ACTIVO',
            'departamento': self.departamento.pk, 'cargo': self.cargo.pk,
            'capacitaciones': [],
        })
        self.assertFalse(form.is_valid())
        self.assertIn('cedula', form.errors)
