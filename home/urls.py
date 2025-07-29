from django.urls import path
from . import views
from .views import contacto

urlpatterns= [
    path("", views.home_view, name="home"),
    path("contacto/", contacto, name="contacto"),
]
