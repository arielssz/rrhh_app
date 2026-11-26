
from django import forms
from personal.models import Cargo


class CargoForm(forms.ModelForm):

    class Meta:
        model = Cargo
        fields = ['nombre', 'descripcion', 'salario_base', 'activo']

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'salario_base': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
