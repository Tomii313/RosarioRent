from django.urls import path
from . import views

urlpatterns = [
    path('', views.oficinas_view, name='oficinas'),
    #path("departamento/<int:id>/", views.departamento_informacion, name="departamento_informacion") 
    path("oficinas/<int:id>/", views.oficinas_informacion, name="oficinas_informacion"),
    path('publicar/', views.publicar_oficina, name='publicar_oficina'),
    
]

