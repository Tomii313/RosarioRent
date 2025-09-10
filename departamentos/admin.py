from django.contrib import admin
from .models import Departamentos, ImagenDepartamento
# Register your models here.
admin.site.register(Departamentos)
admin.site.register(ImagenDepartamento)


class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'precio', 'habitaciones', 'banos', 'disponibilidad', 'aprobado')
    list_filter = ('disponibilidad', 'aprobado')
    list_editable = ('disponibilidad', 'aprobado')