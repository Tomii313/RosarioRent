from django import forms
from .models import salones

class FormularioSalones(forms.ModelForm):
    class Meta:
        model = salones
        exclude = ['propietario', 'fecha_publicacion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', "oninput": "if(this.value.length > 50) this.value=this.value.slice(0,50);"}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control', "oninput": "if(this.value.length > 30) this.value=this.value.slice(0,30);"}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', "oninput": "if(this.value.length > 9) this.value=this.value.slice(0,9);"}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', "oninput": 'if(this.value.length > 800) this.value=this.value.slice(0,800);'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 100000, "oninput": "if(this.value.length > 5) this.value=this.value.slice(0,5);"}),
           # 'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
        }
        