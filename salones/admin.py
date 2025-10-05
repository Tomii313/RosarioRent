from django.contrib import admin
from .models import salones, ImagenSalon

# Inline para manejar las imágenes dentro del admin de Salones
class ImagenSalonInline(admin.TabularInline):   # o admin.StackedInline
    model = ImagenSalon
    extra = 1            # cuántos campos vacíos mostrar por defecto
    fields = ('imagen',)  # solo el campo que queremos mostrar

# Admin personalizado para Salones
@admin.register(salones)
class SalonesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'capacidad', 'precio', 'aprobado')
    inlines = [ImagenSalonInline]

# Ya no registramos ImagenSalon por separado