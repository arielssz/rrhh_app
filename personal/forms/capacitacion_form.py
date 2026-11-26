
from django import forms
from django.core.exceptions import ValidationError
from personal.models import Capacitacion


class CapacitacionForm(forms.ModelForm):

    class Meta:
        model = Capacitacion

        fields = [
            'nombre',
            'descripcion',
            'modalidad',
            'fecha_inicio',
            'fecha_fin',
            'duracion_horas',
            'activa',
        ]

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la capacitación'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'modalidad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'duracion_horas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'activa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_fecha_fin(self):
        fecha_fin = self.cleaned_data.get('fecha_fin')
        fecha_inicio = self.cleaned_data.get('fecha_inicio')
        if fecha_inicio and fecha_fin and fecha_fin < fecha_inicio:
            raise ValidationError('La fecha de finalización no puede ser anterior a la fecha de inicio.')
        return fecha_fin
