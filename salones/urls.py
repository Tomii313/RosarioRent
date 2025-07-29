from django.urls import path
from . import views

urlpatterns = [
    path('', views.salones_view, name='salones')
    #path("departamento/<int:id>/", views.departamento_informacion, name="departamento_informacion") 
]

