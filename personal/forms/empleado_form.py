
from django import forms
from django.core.exceptions import ValidationError
from personal.models import Empleado


class EmpleadoForm(forms.ModelForm):

    class Meta:
        model = Empleado

        fields = [
            'cedula',
            'nombres',
            'apellidos',
            'email',
            'telefono',
            'fecha_nacimiento',
            'fecha_contratacion',
            'estado',
            'departamento',
            'cargo',
            'capacitaciones',
        ]

        widgets = {
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese la cédula'
            }),
            'nombres': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese los nombres'
            }),
            'apellidos': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese los apellidos'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de teléfono'
            }),
            'fecha_nacimiento': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'fecha_contratacion': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'departamento': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cargo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'capacitaciones': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '4'
            }),
        }

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula', '')
        if not cedula.isdigit() or len(cedula) != 10:
            raise ValidationError('La cédula debe contener exactamente 10 dígitos.')
        return cedula
