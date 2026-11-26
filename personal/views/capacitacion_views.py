from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from personal.forms import CapacitacionForm
from personal.models import Capacitacion


@login_required
@permission_required('personal.view_capacitacion', raise_exception=True)
def capacitacion_lista(request):
    return render(request, 'personal/capacitacion/lista.html', {
        'capacitaciones': Capacitacion.objects.all()
    })


@login_required
@permission_required('personal.view_capacitacion', raise_exception=True)
def capacitacion_detalle(request, pk):
    capacitacion = get_object_or_404(Capacitacion, pk=pk)
    return render(request, 'personal/capacitacion/detalle.html', {'capacitacion': capacitacion})


@login_required
@permission_required('personal.add_capacitacion', raise_exception=True)
def capacitacion_crear(request):
    if request.method == 'POST':
        form = CapacitacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Capacitación creada correctamente.')
            return redirect('personal:capacitacion_lista')
    else:
        form = CapacitacionForm()
    return render(request, 'personal/capacitacion/formulario.html', {
        'form': form, 'titulo': 'Registrar capacitación'
    })


@login_required
@permission_required('personal.change_capacitacion', raise_exception=True)
def capacitacion_editar(request, pk):
    capacitacion = get_object_or_404(Capacitacion, pk=pk)
    if request.method == 'POST':
        form = CapacitacionForm(request.POST, instance=capacitacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Capacitación actualizada correctamente.')
            return redirect('personal:capacitacion_lista')
    else:
        form = CapacitacionForm(instance=capacitacion)
    return render(request, 'personal/capacitacion/formulario.html', {
        'form': form, 'titulo': 'Editar capacitación'
    })


@login_required
@permission_required('personal.delete_capacitacion', raise_exception=True)
def capacitacion_eliminar(request, pk):
    capacitacion = get_object_or_404(Capacitacion, pk=pk)
    if request.method == 'POST':
        capacitacion.delete()
        messages.success(request, 'Capacitación eliminada correctamente.')
        return redirect('personal:capacitacion_lista')
    return render(request, 'personal/capacitacion/confirmar_eliminacion.html', {
        'capacitacion': capacitacion
    })
