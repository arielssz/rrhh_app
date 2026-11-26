from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from personal.forms import CargoForm
from personal.models import Cargo


@login_required
@permission_required('personal.view_cargo', raise_exception=True)
def cargo_lista(request):
    return render(request, 'personal/cargo/lista.html', {'cargos': Cargo.objects.all()})


@login_required
@permission_required('personal.view_cargo', raise_exception=True)
def cargo_detalle(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    return render(request, 'personal/cargo/detalle.html', {'cargo': cargo})


@login_required
@permission_required('personal.add_cargo', raise_exception=True)
def cargo_crear(request):
    if request.method == 'POST':
        form = CargoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo creado correctamente.')
            return redirect('personal:cargo_lista')
    else:
        form = CargoForm()
    return render(request, 'personal/cargo/formulario.html', {'form': form, 'titulo': 'Crear cargo'})


@login_required
@permission_required('personal.change_cargo', raise_exception=True)
def cargo_editar(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cargo actualizado correctamente.')
            return redirect('personal:cargo_lista')
    else:
        form = CargoForm(instance=cargo)
    return render(request, 'personal/cargo/formulario.html', {'form': form, 'titulo': 'Editar cargo'})


@login_required
@permission_required('personal.delete_cargo', raise_exception=True)
def cargo_eliminar(request, pk):
    cargo = get_object_or_404(Cargo, pk=pk)
    if request.method == 'POST':
        cargo.delete()
        messages.success(request, 'Cargo eliminado correctamente.')
        return redirect('personal:cargo_lista')
    return render(request, 'personal/cargo/confirmar_eliminacion.html', {'cargo': cargo})
