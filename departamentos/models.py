from django.db import models
from django.conf import settings

# Create your models here.
class Departamentos(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    piso = models.IntegerField(null=True, blank=True)
    departamento = models.IntegerField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="departamentos/", blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    habitaciones = models.IntegerField()
    banos = models.IntegerField()
    disponibilidad = models.BooleanField(default=True)
    zona = models.CharField(max_length=50, null=True, blank=True)
   

    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="departamentos",
        null=True,  blank=True
    )

    def __str__(self):
        return f"{self.nombre} - {self.direccion} - {self.precio}"
    
    class Meta:
         verbose_name = "Departamento"
         verbose_name_plural = "Departamentos"

class ImagenDepartamento(models.Model):
    departamento = models.ForeignKey(Departamentos, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to="departamentos/imagenes", blank=True, null=True)

    def __str__(self):
        return f"Imagen de {self.departamento.nombre}"
    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imagenes"

        