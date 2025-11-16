from django.db import models
from django.conf import settings
from geopy.geocoders import Nominatim
from cloudinary.models import CloudinaryField
# Create your models here.


BARRIOS = [
    ("Centro", "Centro"),
    ("Macrocentro", "Macrocentro"),
    ("Echesortu", "Echesortu"),
    ("Abasto", "Abasto"),
    ("Tablada", "Tablada"),
    ("Martin", "Martin"),
    ("Las Delicias", "Las Delicias"),
    ("Fisherton", "Fisherton"),
    ("Arroyito", "Arroyito"),
    ("Pichincha", "Pichincha"),
    ("Luis Agote", "Luis Agote"),
    ("Alberdi", "Alberdi"),
    ("Empalme Graneros", "Empalme Graneros"),
    ("Ludueña", "Ludueña"),
    ("Belgrano", "Belgrano"),
    ("Azcuénaga", "Azcuénaga"),
    ("Refinería", "Refinería"),
    ("Hospitales", "Hospitales"),
    ("La Florida", "La Florida"),
    ("Sarmiento", "Sarmiento"),
    ("Hostal del Sol", "Hostal del Sol"),
    ("Barrio Rucci", "Barrio Rucci"),
    ("Godoy", "Godoy"),
    ("7 de Septiembre", "7 de Septiembre"),
    ("Lisandro de la Torre", "Lisandro de la Torre"),
    ("Antártida Argentina", "Antártida Argentina"),
    ("Lomas de Alberdi", "Lomas de Alberdi"),
    ("Zona Norte", "Norte"),
    ("Zona Oeste", "Oeste"),
    ("Zona Este", "Este"),
    ("Zona Sur", "Sur"),
    ("Zona Suroeste", "Suroeste"),
    ("Zona Sudeste", "Sudeste"),
    ("Villa Gobernador Gálvez", "Villa Gobernador Gálvez"),
    ("Granadero Baigorria", "Granadero Baigorria"),
    ("San Lorenzo", "San Lorenzo"),
    ("Fray Luis Beltrán", "Fray Luis Beltrán"),
    ("Ricardone", "Ricardone"),
    ("Funes", "Funes"),
    ("Roldán", "Roldán"),
    ("Soldini", "Soldini"),
    ("Perez", "Pérez"),
    ("Puente Gallego", "Puente Gallego"),
    
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
    imagen = CloudinaryField('imagen', null=True, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
  
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
    imagen = CloudinaryField('imagen', null=True, blank=True)

    def __str__(self):
        return f"Imagen de {self.salon.nombre}"