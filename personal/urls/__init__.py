from django.urls import path
from personal.views import departamento_views, cargo_views, empleado_views
from personal.views import capacitacion_views

app_name = 'personal'

urlpatterns = [
    # Departamentos
    path('departamentos/', departamento_views.departamento_lista, name='departamento_lista'),
    path('departamentos/nuevo/', departamento_views.departamento_crear, name='departamento_crear'),
    path('departamentos/<int:pk>/', departamento_views.departamento_detalle, name='departamento_detalle'),
    path('departamentos/<int:pk>/editar/', departamento_views.departamento_editar, name='departamento_editar'),
    path('departamentos/<int:pk>/eliminar/', departamento_views.departamento_eliminar, name='departamento_eliminar'),

    # Cargos
    path('cargos/', cargo_views.cargo_lista, name='cargo_lista'),
    path('cargos/nuevo/', cargo_views.cargo_crear, name='cargo_crear'),
    path('cargos/<int:pk>/', cargo_views.cargo_detalle, name='cargo_detalle'),
    path('cargos/<int:pk>/editar/', cargo_views.cargo_editar, name='cargo_editar'),
    path('cargos/<int:pk>/eliminar/', cargo_views.cargo_eliminar, name='cargo_eliminar'),

    # Empleados
    path('empleados/', empleado_views.empleado_lista, name='empleado_lista'),
    path('empleados/nuevo/', empleado_views.empleado_crear, name='empleado_crear'),
    path('empleados/<int:pk>/', empleado_views.empleado_detalle, name='empleado_detalle'),
    path('empleados/<int:pk>/editar/', empleado_views.empleado_editar, name='empleado_editar'),
    path('empleados/<int:pk>/eliminar/', empleado_views.empleado_eliminar, name='empleado_eliminar'),
     # Capacitaciones
    path('capacitaciones/', capacitacion_views.capacitacion_lista, name='capacitacion_lista'),
    path('capacitaciones/nuevo/', capacitacion_views.capacitacion_crear, name='capacitacion_crear'),
    path('capacitaciones/<int:pk>/', capacitacion_views.capacitacion_detalle, name='capacitacion_detalle'),
    path('capacitaciones/<int:pk>/editar/', capacitacion_views.capacitacion_editar, name='capacitacion_editar'),
    path('capacitaciones/<int:pk>/eliminar/', capacitacion_views.capacitacion_eliminar, name='capacitacion_eliminar'),	
]
