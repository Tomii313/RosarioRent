from django import forms
from .models import Departamentos, BARRIOS

class FormularioDepartamento(forms.ModelForm):
    zona = forms.ChoiceField(
    choices=[('', '-- 🏠 Seleccione una opción --')] + BARRIOS,
    widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Departamentos
        exclude = ['propietario', 'fecha_publicacion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control' }),
            'precio': forms.NumberInput(attrs={'class': 'form-control' }),
            'descripcion': forms.Textarea(attrs={'class': 'form-control' }),
           # 'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'habitaciones': forms.NumberInput(attrs={'class': 'form-control' }),
            'banos': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 8, 'onkeydown': 'return false;' , 'onpaste': 'return false', 'value':1}),
            'piso': forms.NumberInput(attrs={'class': 'form-control' }),
            'departamento': forms.TextInput(attrs={'class': 'form-control','maxlength': 1 }),
  
    
        }
                    

       