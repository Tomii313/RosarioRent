from django.urls import path
from . import views

urlpatterns = [
    path('', views.salones_view, name='salones'),
    #path("departamento/<int:id>/", views.departamento_informacion, name="departamento_informacion") 
    path("salon/<int:id>/", views.salones_informacion, name="salones_informacion"),
      path('publicar/', views.publicar_salones, name='publicar_salones'),
]

