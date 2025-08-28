from django import forms
from .models import salones

class FormularioSalones(forms.ModelForm):
    class Meta:
        model = salones
        exclude = ['propietario', 'fecha_publicacion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 500, 'onkeydown': 'return false;' , 'onpaste': 'return false', 'value':1}),
           # 'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
        }
        