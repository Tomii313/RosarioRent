from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Oficina(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    ambientes = models.IntegerField(validators=[MinValueValidator(1, message="Debe tener al menos 1 ambiente"), MaxValueValidator(20, message="Seleccione una cantidad correcta")])
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    
class ImagenOficina(models.Model):
    oficina = models.ForeignKey(Oficina, related_name="imagenes", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="oficinas/imagenes/", blank=True, null=False, default='media/oficinas/imagenes/default.jpg')

    def __str__(self):
        return f"Imagen de {self.oficina.nombre}"

