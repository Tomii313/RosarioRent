from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


BARRIOS = [
     ("centro", "Centro"),
    ("macrocentro", "Macrocentro"),
    ("echesortu", "Echesortu"),
    ("abasto", "Abasto"),
    ("tablada", "Tablada"),
    ("las_delicias", "Las Delicias"),
    ("fisherton", "Fisherton"),
    ("arroyito", "Arroyito"),
    ("aladelta", "Alto Rosario"),
    ("pichincha", "Pichincha"),
    ("zona_norte", "Zona Norte"),
    ("zona_oeste", "Zona Oeste"),
    ("zona_este", "Zona Este"),
    ("zona_sur", "Zona Sur"),
    ("zona_suroeste", "Zona Suroeste"),
    ("zona_sudeste", "Zona Sudeste"),
    ("villa_gobernador_galvez", "Villa Gobernador Gálvez"),
    ("granadero_baigorria", "Granadero Baigorria"),
    ("ricardone", "Ricardone"),
    ("san_lorenzo", "San Lorenzo"),
    ("fray_luis_beltran", "Fray Luis Beltrán"),
    ("funes", "Funes"),
    ("roldan", "Roldán"),
    ("soldini", "Soldini"),
    ("perez", "Pérez"),
    ("other", "Otro")

]

class Departamentos(models.Model):
    nombre = models.CharField(max_length=100, validators=[], error_messages={"blank": "El nombre no puede estar vacío", 'null': 'El nombre no puede ser nulo'})
    direccion = models.CharField(max_length=100)
    piso = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0, message="Seleccione un piso correcto") ,MaxValueValidator(20, message="Seleccione un piso correcto")])
    departamento = models.IntegerField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="departamentos/", blank=True, null=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    habitaciones = models.IntegerField(validators=[MinValueValidator(1, message='Debe tener al menos 1 habitación'), MaxValueValidator(20, message="Seleccione una cantidad correcta")])
    banos = models.IntegerField(validators=[MinValueValidator(1, message='Debe tener al menos 1 baño'), MaxValueValidator(8, message="Seleccione una cantidad correcta")])
    disponibilidad = models.BooleanField(default=True)
    zona = models.CharField(max_length=50, null=True, blank=True, choices=BARRIOS)
   

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



        