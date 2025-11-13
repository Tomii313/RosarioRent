from django.contrib import admin
from .models import UsuarioPersonalizado
# Register your models here.
""" admin.site.register(UsuarioPersonalizado) """

@admin.register(UsuarioPersonalizado)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nombre","dni", "email", "baneado")
    search_fields = ['dni', "email"]
    list_editable = ['baneado']


