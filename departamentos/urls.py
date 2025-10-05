from django.urls import path
from . import views

urlpatterns = [
    path('', views.alquileres, name='departamentos'), 
    path("departamento/<int:id>/", views.departamento_informacion, name="departamentos_informacion"), 
    path('publicar/', views.publicar_departamento, name='publicar_departamento'),
    path('contactar/<int:publicacion_id>/', views.contactar_propietario, name='contactar_departamento'),
    path('eliminar/<int:id>/',views.eliminarpublicacion, name="eliminar_departamento"),
    

]

