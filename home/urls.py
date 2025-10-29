from django.urls import path
from . import views
from .views import contacto

urlpatterns= [
    path("", views.home_view, name="home"),
    path("contacto/", contacto, name="contacto"),
    path('chatbot/', views.chatbot, name='chatbot'), 
    path('terminos/', views.terminos, name="terminos"),
    path('Error_404/', views.error_404, name='error_404'),
]
