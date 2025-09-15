from django.urls import path
from . import views

urlpatterns = [
  #  path("<str:modelo>/<int:id>/", views.detalle_publicacion, name="detalle_publicacion"),
    path("baneado/", views.baneado, name="baneado")
]