from .models import salones, ImagenSalon
from django.contrib import admin

admin.site.register(salones)
admin.site.register(ImagenSalon)

# Register your models here.
# The above code registers the 'salones' and 'ImagenSalon' models with the Django
# admin site, allowing them to be managed through the Django admin interface.
# This enables the admin interface to display and manage instances of these models.
# The 'salones' model represents a salon with attributes like name, location, capacity,
# description, price, availability, and publication date.
