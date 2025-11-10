from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from usuarios.models import UsuarioPersonalizado
from django.contrib.auth import get_user_model
from multiselectfield import MultiSelectFormField
from django.forms.widgets import CheckboxInput
User = get_user_model()

class FormularioRegistro(UserCreationForm):

    email = forms.EmailField(
        label= "Correo",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            'required':True,
            "placeholder": "Ingresa tu correo electrónico"

        })
    )
    
    username = forms.CharField(
    label="Usuario",
    widget=forms.TextInput(attrs={
        "class":"form-control",
        'required':True,
        "placeholder":"Ingresa tu nombre de usuario"
        
    })
    )

    nombre = forms.CharField(
        label="Nombres", widget=forms.TextInput(attrs={
            "class": "form-control",
            'required':True,
            "placeholder": "Ingresa tu/s nombre/s"

        })
    )
    
    apellido = forms.CharField(
        label="Apellido", widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ingresa tu/s apellido/s",
            'required':True,

        })
    )
    
    dni = forms.CharField(
        label="DNI", widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "DNI",
            "min":"0", "maxlength":"8",
            'required':True,

            "oninput:": "if(this.value.length > 8) this.value=this.value.slice(0,5);"
        })
    )
    
    telefono = forms.CharField(
        label="Telefono", widget=forms.TextInput(attrs={
            "class": "form-control",
            'required':True,
            "placeholder": "Ingresa tu teléfono"

        })
    )
    
    direccion = forms.CharField(
        label="Dirección", widget=forms.TextInput(attrs={
            "class": "form-control",
            'required':True,
            "placeholder": "Ingresa tu dirección"

        })
    )
    
    num_calle = forms.IntegerField(
        label="Número de Calle", widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "NRO",
            "min": "0", "max":"10000","maxlength":"5",
            'required':True,
            "oninput": "if(this.value.length > 5) this.value = this.value.slice(0,5);"

        })
    )
    nacimiento = forms.DateField(
        label="Fecha de Nacimiento", widget=forms.DateInput(attrs={
            "class": "form-control",
            "placeholder": "Ingresa tu fecha de nacimiento",
            "type":"date",
            'required':True,
            "max": "2010-12-31"

        })
    )
    
 
    password1 = forms.CharField(
    label="Contraseña",
    widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresá tu contraseña'

        })
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña',
            'required':True
        })
    )

    tipo = forms.ChoiceField(
        label = "Tipo de usuario",
        choices=UsuarioPersonalizado.TIPO_USUARIO,
        widget=forms.Select(attrs={
            "class": "form-control"})

        )
    
    tipo_publicacion = MultiSelectFormField(
        label="Tipo de propiedad que puede publicar",
        choices=UsuarioPersonalizado.TIPO_PUBLICACION,
        required=False,
       
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"})
)
    class Meta:
        model = UsuarioPersonalizado
        fields = ["email","username", "nombre", "apellido", "dni", "direccion", "num_calle", "telefono", "nacimiento", "password1", "password2", "tipo", 'tipo_publicacion']


class AuthenticationForm(AuthenticationForm):
      username= forms.EmailField(
        label="Correo",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Ingrese su correo"
        })

      )
      password = forms.CharField(
            label="Contraseña",
            widget=forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Ingresa tu contraseña"
            })
        )

      
