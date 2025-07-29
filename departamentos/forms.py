from django import forms
from .models import Departamentos

class FormularioDepartamento(forms.ModelForm):
    class Meta:
        model = Departamentos
        exclude = ['propietario', 'fecha_publicacion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
           # 'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'habitaciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'banos': forms.NumberInput(attrs={'class': 'form-control'}),
            'piso': forms.NumberInput(attrs={'class': 'form-control'}),
            'departamento': forms.NumberInput(attrs={'class': 'form-control'}),
             'zona': forms.TextInput(attrs={'class': 'form-control'})
        }
        