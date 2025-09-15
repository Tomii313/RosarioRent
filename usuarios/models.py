from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
# Create your models here.

class UsuarioPersonalizado(AbstractUser):
    TIPO_USUARIO = (
        ('inquilino', 'inquilino'),
        ('propietario', 'propietario'),
 
    )

    TIPO_PUBLICACION = (
        ('departamento', 'Departamentos'),
        ('oficina','Oficinas'),
        ('salon', 'Salones'),
    )
    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=250)
    dni = models.CharField(max_length=30, unique=True)
    

    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, default='inquilino')
    tipo_publicacion = models.CharField(max_length=20, choices=TIPO_PUBLICACION, blank=True, null=True)


    baneado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.apellido}"


class Comentario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    estrellas = models.IntegerField(default=5)
    creado = models.DateTimeField(auto_now_add=True)

    #Enlace Genérico
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    publicacion = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.usuario.username} - {self.publicacion} {self.estrellas}"


class Favorito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    publicacion = GenericForeignKey("content_type", "object_id")
    agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.publicacion}"

  