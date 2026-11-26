from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils.http import url_has_allowed_host_and_scheme

from personal.forms import RegistroForm


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    destino = request.GET.get('next') or request.POST.get('next') or settings.LOGIN_REDIRECT_URL
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, f'Bienvenido, {usuario.username}.')
            if not url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}):
                destino = settings.LOGIN_REDIRECT_URL
            return redirect(destino)
    else:
        form = AuthenticationForm(request)

    return render(request, 'registration/login.html', {'form': form, 'next': destino})


def registro(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            grupo, _ = Group.objects.get_or_create(name='Consultor')
            usuario.groups.add(grupo)
            messages.success(request, 'Cuenta creada correctamente. Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()

    return render(request, 'registration/registro.html', {'form': form})


@require_POST
def cerrar_sesion(request):
    logout(request)
    messages.success(request, 'Sesión cerrada correctamente.')
    return redirect(settings.LOGOUT_REDIRECT_URL)
