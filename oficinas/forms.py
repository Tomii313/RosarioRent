from django import forms
from .models import Oficina

class FormularioOficinas(forms.ModelForm):
    class Meta:
        model = Oficina
        exclude = ['propietario', 'fecha_publicacion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'ambientes': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
           # 'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
        }
        