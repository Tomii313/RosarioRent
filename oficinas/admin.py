from django.contrib import admin
from .models import Oficina, ImagenOficina

class ImagenOficinaInline(admin.TabularInline):  
    model = ImagenOficina
    extra = 1  # cuántos campos vacíos aparecen por defecto
    fields = ['imagen']
    readonly_fields = []

@admin.register(Oficina)
class OficinaAdmin(admin.ModelAdmin):
    list_display = ('direccion', 'ambientes', 'precio', 'disponible', 'aprobado')
    list_filter = ('disponible', 'aprobado', 'monedas')
    search_fields = ('direccion', 'descripcion')
    inlines = [ImagenOficinaInline]  # 👉 esto agrega la galería de imágenes en la misma pantalla

@admin.register(ImagenOficina)
class ImagenOficinaAdmin(admin.ModelAdmin):
    list_display = ('oficina', 'imagen')