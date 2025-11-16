from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from multiselectfield import MultiSelectField
from cloudinary.models import CloudinaryField
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
    dni = models.CharField(max_length=30, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    num_calle = models.IntegerField(validators=[MinValueValidator(0, message="El número no puede ser menor a 0."), MaxValueValidator(10000, message="El número no puede ser mayor a 10.000")], null=True, blank=True)
    nacimiento = models.DateField(null=True, blank=True)
    imagen = CloudinaryField('imagen', null=True, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, default='inquilino')
    #tipo_publicacion = models.CharField(max_length=20, choices=TIPO_PUBLICACION, blank=True, null=True)
    tipo_publicacion = MultiSelectField(choices=TIPO_PUBLICACION, blank=True)

    USERNAME_FIELD = 'email'  # <--- esto hace que Django use email para login
    REQUIRED_FIELDS = ['username']  # username sigue existiendo pero no para login


    baneado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} {self.dni} {self.email}"


class Comentario(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    estrellas = models.IntegerField(default=5)
    creado = models.DateTimeField(auto_now_add=True)

    #Enlace Genérico
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    publicacion = GenericForeignKey("content_type", "object_id")

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="respuestas")
    def __str__(self):
        return f"{self.usuario.nombre} - {self.publicacion} {self.estrellas}"


class Favorito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    publicacion = GenericForeignKey("content_type", "object_id")
    agregado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.publicacion}"

  