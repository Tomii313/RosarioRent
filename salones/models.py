from django.db import models
from django.conf import settings

# Create your models here.


BARRIOS = [
     ("Centro", "Centro"),
    ("Macrocentro", "Macrocentro"),
    ("Echesortu", "Echesortu"),
    ("Abasto", "Abasto"),
    ("Tablada", "Tablada"),
    ("Las Delicias", "Las Delicias"),
    ("Fisherton", "Fisherton"),
    ("Arroyito", "Arroyito"),
    ("Pichincha", "Pichincha"),
    ("Zona Norte", "Norte"),
    ("Zona Oeste", "Oeste"),
    ("Zona Este", "Este"),
    ("Zona Sur", "Sur"),
    ("Zona Suroeste", "Suroeste"),
    ("Zona Sudeste", "Sudeste"),
    ("Villa Gobernador Gálvez", "Villa Gobernador Gálvez"),
    ("Granadero Baigorria", "Granadero Baigorria"),
    ("Ricardone", "Ricardone"),
    ("San Lorenzo", "San Lorenzo"),
    ("Fray Luis Beltrán", "Fray Luis Beltrán"),
    ("Funes", "Funes"),
    ("Roldán", "Roldán"),
    ("Soldini", "Soldini"),
    ("Pérez", "Pérez"),
    ("Otro", "Otro")

]

class salones(models.Model):
    MONEDAS = [
    ('ARS', 'Pesos Argentinos (ARS)'),
    ('USD', 'Dólares (USD)'),
    ]
    nombre = models.CharField(max_length=100)
    zona = models.CharField(max_length=50, null=True, blank=True, choices=BARRIOS)
    direccion = models.CharField(max_length=200)
    capacidad = models.IntegerField()
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    monedas = models.CharField(max_length=3, choices=MONEDAS, default="ARS")
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to="salones/", blank=True, null=True)
  
    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="salones",
        null=True,  blank=True
    )
    
    def __str__(self):
        return f"{self.nombre} - {self.direccion} - {self.capacidad} - {self.precio}"



class ImagenSalon(models.Model):
    salon = models.ForeignKey(salones, related_name="imagenes", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="salones/imagenes/", blank=True, null=True)

    def __str__(self):
        return f"Imagen de {self.salon.nombre}"