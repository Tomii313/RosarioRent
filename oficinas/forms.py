from django import forms
from .models import Oficina

class FormularioOficinas(forms.ModelForm):
    class Meta:
        model = Oficina
        exclude = ['propietario', 'fecha_publicacion', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control',"oninput": "if(this.value.length > 100) this.value=this.value.slice(0,100);"}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', "maxlength":"40",'oninput': 'if(this.value.length > 40) this.value=this.value.slice(0,40);'}),
            'ambientes': forms.NumberInput(attrs={'class': 'form-control', "min":"1", "max":"10",
            "oninput": "if(this.value.length > 2) this.value=this.value.slice(0,2);"}),
            'piso': forms.NumberInput(attrs={'class': 'form-control', "min":"1", "max":"10",
            "oninput": "if(this.value.length > 2) this.value=this.value.slice(0,2);"}),
            'precio': forms.NumberInput(attrs={'class': 'form-control' ,"oninput": "if(this.value.length > 9) this.value=this.value.slice(0,9);"}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'oninput': 'if(this.value.length > 800) this.value=this.value.slice(0,800);'}),
           # 'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
        }
        