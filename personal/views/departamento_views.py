from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from personal.forms import DepartamentoForm
from personal.models import Departamento


@login_required
@permission_required('personal.view_departamento', raise_exception=True)
def departamento_lista(request):
    return render(request, 'personal/departamento/lista.html', {
        'departamentos': Departamento.objects.all()
    })


@login_required
@permission_required('personal.view_departamento', raise_exception=True)
def departamento_detalle(request, pk):
    departamento = get_object_or_404(Departamento, pk=pk)
    return render(request, 'personal/departamento/detalle.html', {'departamento': departamento})


@login_required
@permission_required('personal.add_departamento', raise_exception=True)
def departamento_crear(request):
    if request.method == 'POST':
        form = DepartamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento creado correctamente.')
            return redirect('personal:departamento_lista')
    else:
        form = DepartamentoForm()
    return render(request, 'personal/departamento/formulario.html', {
        'form': form, 'titulo': 'Crear departamento'
    })


@login_required
@permission_required('personal.change_departamento', raise_exception=True)
def departamento_editar(request, pk):
    departamento = get_object_or_404(Departamento, pk=pk)
    if request.method == 'POST':
        form = DepartamentoForm(request.POST, instance=departamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Departamento actualizado correctamente.')
            return redirect('personal:departamento_lista')
    else:
        form = DepartamentoForm(instance=departamento)
    return render(request, 'personal/departamento/formulario.html', {
        'form': form, 'titulo': 'Editar departamento'
    })


@login_required
@permission_required('personal.delete_departamento', raise_exception=True)
def departamento_eliminar(request, pk):
    departamento = get_object_or_404(Departamento, pk=pk)
    if request.method == 'POST':
        departamento.delete()
        messages.success(request, 'Departamento eliminado correctamente.')
        return redirect('personal:departamento_lista')
    return render(request, 'personal/departamento/confirmar_eliminacion.html', {
        'departamento': departamento
    })
