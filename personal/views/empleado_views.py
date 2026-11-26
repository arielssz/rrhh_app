
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from personal.models import Empleado
from personal.forms import EmpleadoForm


@login_required
@permission_required('personal.view_empleado', raise_exception=True)
def empleado_lista(request):
    empleados = Empleado.objects.all()

    return render(
        request,
        'personal/empleado/lista.html',
        {'empleados': empleados}
    )


@login_required
@permission_required('personal.view_empleado', raise_exception=True)
def empleado_detalle(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)

    return render(
        request,
        'personal/empleado/detalle.html',
        {'empleado': empleado}
    )


@login_required
@permission_required('personal.add_empleado', raise_exception=True)
def empleado_crear(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)

        if form.is_valid():
            empleado = form.save(commit=False)
            empleado.creado_por = request.user
            empleado.save()
            form.save_m2m()

            messages.success(request, 'Empleado creado correctamente.')
        return redirect('personal:empleado_lista')

    else:
        form = EmpleadoForm()

    return render(
        request,
        'personal/empleado/formulario.html',
        {'form': form, 'titulo': 'Registrar empleado'}
    )


@login_required
@permission_required('personal.change_empleado', raise_exception=True)
def empleado_editar(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)

    # Los administradores pueden editar cualquier empleado.
    # Los consultores solamente pueden editar los que registraron.
    if (
        not request.user.has_perm('personal.delete_empleado')
        and empleado.creado_por_id != request.user.id
    ):
        raise PermissionDenied

    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)

        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado actualizado correctamente.')
            return redirect('personal:empleado_lista')

    else:
        form = EmpleadoForm(instance=empleado)

    return render(
        request,
        'personal/empleado/formulario.html',
        {'form': form, 'titulo': 'Editar empleado'}
    )


@login_required
@permission_required('personal.delete_empleado', raise_exception=True)
def empleado_eliminar(request, pk):
    empleado = get_object_or_404(Empleado, pk=pk)

    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado correctamente.')
        return redirect('personal:empleado_lista')

    return render(
        request,
        'personal/empleado/confirmar_eliminacion.html',
        {'empleado': empleado}
    )
