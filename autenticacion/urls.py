from django.urls import path
from . views import VRegistro, VLogin
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', VRegistro.as_view(), name='autenticacion'),
    #path("departamento/<int:id>/", views.departamento_informacion, name="departamento_informacion") 
    path("login/", VLogin.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
]

