from django.contrib import admin
from .models import Departamentos, ImagenDepartamento


class ImagenDepartamentoInline(admin.TabularInline):
    model = ImagenDepartamento
    extra = 1              # cuántos campos vacíos muestra por defecto
    fields = ['imagen']    # solo muestra el campo de la imagen


@admin.register(Departamentos)
class DepartamentosAdmin(admin.ModelAdmin):
    list_display = ('direccion', 'precio', 'habitaciones', 'banos', 'disponibilidad', 'aprobado')
    list_filter = ('disponibilidad', 'aprobado', 'zona', 'monedas')
    list_editable = ('disponibilidad', 'aprobado')
    #search_fields = ('nombre', 'direccion')
    inlines = [ImagenDepartamentoInline]   # 👉 galería de imágenes en la misma pantalla del admin


@admin.register(ImagenDepartamento)
class ImagenDepartamentoAdmin(admin.ModelAdmin):
    list_display = ('departamento', 'imagen')