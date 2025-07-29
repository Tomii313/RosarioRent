from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UsuarioPersonalizado(AbstractUser):
    TIPO_USUARIO = (
        ('inquilino', 'inquilino'),
        ('propietario', 'propietario'),
 
    )

    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, default='inquilino')