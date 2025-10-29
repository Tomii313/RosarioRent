from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from geopy.geocoders import Nominatim

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
    ("Roldan", "Roldán"),
    ("Soldini", "Soldini"),
    ("Perez", "Pérez"),
    ("Otro", "Otro")

]



class Departamentos(models.Model):
    MONEDAS = [
    ('ARS', 'Pesos Argentinos (ARS)'),
    ('USD', 'Dólares (USD)'),
    ]
    nombre = models.CharField(null=True, blank=True,max_length=100, validators=[], error_messages={"blank": "El nombre no puede estar vacío", 'null': 'El nombre no puede ser nulo'})
    direccion = models.CharField(max_length=100)
    piso = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0, message="Seleccione un piso correcto") ,MaxValueValidator(20, message="Seleccione un piso correcto")])
    departamento = models.CharField(max_length=2,null=True, blank=True)
    precio = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)])
    monedas = models.CharField(max_length=3, choices=MONEDAS, default="ARS")
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="departamentos/", blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    habitaciones = models.IntegerField(validators=[MinValueValidator(0, message='Inserte un valor valido'), MaxValueValidator(20, message="Seleccione una cantidad correcta")])
    banos = models.IntegerField(validators=[MinValueValidator(1, message='Debe tener al menos 1 baño'), MaxValueValidator(8, message="Seleccione una cantidad correcta")])
    disponibilidad = models.BooleanField(default=True)
    aprobado = models.BooleanField(default=False)
    zona = models.CharField(max_length=50, null=True, blank=True, choices=BARRIOS)
    

   

    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="departamentos",
        null=True,  blank=True
    )

    def __str__(self):
        return f"{self.propietario.nombre} - {self.direccion} - {self.precio} - {self.monedas}"
    
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



        