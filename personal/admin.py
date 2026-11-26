from django.contrib import admin
from personal.models import Departamento, Cargo, Empleado, Capacitacion


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'fecha_creacion')
    search_fields = ('nombre',)
    list_filter = ('activo',)


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'salario_base', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombres', 'apellidos', 'departamento', 'cargo', 'estado')
    search_fields = ('cedula', 'nombres', 'apellidos')
    list_filter = ('estado', 'departamento', 'cargo')


@admin.register(Capacitacion)
class CapacitacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'modalidad', 'fecha_inicio', 'fecha_fin', 'activa')
    search_fields = ('nombre',)
    list_filter = ('modalidad', 'activa')
