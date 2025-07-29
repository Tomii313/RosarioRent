from django.urls import path
from . import views

urlpatterns = [
    path('', views.alquileres, name='departamentos'), 
    path("departamento/<int:id>/", views.departamento_informacion, name="departamento_informacion"), 
    path('publicar/', views.publicar_departamento, name='publicar_departamento'),
    path('contactar/<int:publicacion_id>/', views.contactar_propietario, name='contactar_propietario'),
]

