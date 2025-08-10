from django.db import models

# Create your models here.

class salones(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    capacidad = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to="salones/", blank=True, null=True)
  

    def __str__(self):
        return f"{self.nombre} - {self.ubicacion} - {self.capacidad} - {self.precio}"



class ImagenSalon(models.Model):
    salon = models.ForeignKey(salones, related_name="imagenes", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="salones/imagenes/", blank=True, null=True)

    def __str__(self):
        return f"Imagen de {self.salon.nombre}"