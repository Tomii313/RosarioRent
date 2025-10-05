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
           # 'nombre': forms.TextInput(attrs={'class': 'form-control', "oninput": "if(this.value.length > 100) this.value=this.value.slice(0,100);"}),
            'direccion': forms.TextInput(attrs={'class': 'form-control',"oninput": "if(this.value.length > 30) this.value=this.value.slice(0,30);" }),
            'precio': forms.NumberInput(attrs={'class': 'form-control', "oninput": "if(this.value.length > 9) this.value=this.value.slice(0,9);" }),
            'monedas': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control','oninput': 'if(this.value.length > 800) this.value=this.value.slice(0,800);' }),
           # 'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'habitaciones': forms.NumberInput(attrs={'class': 'form-control','max':10,'oninput': 'if(this.value.length > 1) this.value=this.value.slice(0,1);' }),
            'banos': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 4, 'value':1, 'oninput': 'if(this.value.length > 1) this.value=this.value.slice(0,1);'}),
            'piso': forms.NumberInput(attrs={'class': 'form-control', 'oninput': 'if(this.value.length > 2) this.value=this.value.slice(0,2);' }),
            'departamento': forms.TextInput(attrs={'class': 'form-control','oninput': 'if(this.value.length > 2) this.value=this.value.slice(0,2);' }),
  
    
        }
                    

       