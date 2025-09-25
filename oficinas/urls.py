from django.urls import path
from . import views

urlpatterns = [
    path('', views.alquileres, name='oficinas'),
    #path("departamento/<int:id>/", views.departamento_informacion, name="departamento_informacion") 
    path("oficinas/<int:id>/", views.oficinas_informacion, name="oficina_informacion"),
    path('publicar/', views.publicar_oficina, name='publicar_oficina'),
    path('contactar/<int:publicacion_id>/', views.contactar_propietario, name='contactar_propietario'),
    path('eliminar/<int:id>/',views.eliminarpublicacion, name="eliminar_oficina")
    
]

