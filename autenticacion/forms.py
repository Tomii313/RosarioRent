from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from usuarios.models import UsuarioPersonalizado
from django.contrib.auth import get_user_model

User = get_user_model()

class FormularioRegistro(UserCreationForm):

    email = forms.EmailField(
        label= "Correo",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Ingresa tu correo electrónico"
        })
    )
    username = forms.CharField(
    label="Usuario",
    widget=forms.TextInput(attrs={
        "class":"form-control",
        "placeholder":"Ingresa tu nombre de usuario"
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
            'placeholder': 'Confirma tu contraseña'
        })
    )

    tipo = forms.ChoiceField(
        label = "Tipo de usuario",
        choices=UsuarioPersonalizado.TIPO_USUARIO,
        widget=forms.Select(attrs={
            "class": "form-control"})
        )
    class Meta:
        model = UsuarioPersonalizado
        fields = ["email","username", "password1", "password2", "tipo"]


class AuthenticationForm(AuthenticationForm):
      username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ingresa tu nombre de usuario"
        })

      )
      password = forms.CharField(
            label="Contraseña",
            widget=forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Ingresa tu contraseña"
            })
        )
class Meta:
        model = UsuarioPersonalizado
        fields = ["email","username", "password1", "password2", "tipo"]

