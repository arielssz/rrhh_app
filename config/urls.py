from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from personal.views import auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.iniciar_sesion, name='login'),
    path('accounts/logout/', auth_views.cerrar_sesion, name='logout'),
    path('registro/', auth_views.registro, name='registro'),
    path('', RedirectView.as_view(url='/empleados/', permanent=False), name='inicio'),
    path('', include('personal.urls')),
]
