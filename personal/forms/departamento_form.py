
from django import forms
from personal.models import Departamento


class DepartamentoForm(forms.ModelForm):

    class Meta:
        model = Departamento
        fields = ['nombre', 'descripcion', 'activo']

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del departamento'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
