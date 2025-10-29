from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
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
    ("Roldan", "Roldán"),
    ("Soldini", "Soldini"),
    ("Perez", "Pérez"),
    ("Otro", "Otro")

]


class Oficina(models.Model):
    MONEDAS = [
    ('ARS', 'Pesos Argentinos (ARS)'),
    ('USD', 'Dólares (USD)'),
    ]
    #nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ambientes = models.IntegerField(validators=[MinValueValidator(1, message="Debe tener al menos 1 ambiente"), MaxValueValidator(20, message="Seleccione una cantidad correcta")])
    piso = models.IntegerField(null=True, blank=True)
    departamento = models.CharField(max_length=2,null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)
    monedas = models.CharField(max_length=3, choices=MONEDAS, default="ARS")
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    aprobado = models.BooleanField(default=False)
    zona = models.CharField(max_length=50, null=True, blank=True, choices=BARRIOS)

    propietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="Oficina",
        null=True,  blank=True
    )
    

    def __str__(self):
        return f"{self.propietario.nombre} - {self.direccion} - {self.ambientes} - {self.precio}"
class ImagenOficina(models.Model):
    oficina = models.ForeignKey(Oficina, related_name="imagenes", on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="oficinas/imagenes/", blank=True, null=False, default='media/oficinas/imagenes/default.jpg')

    def __str__(self):
        return f"Imagen de {self.oficina.direccion}"

