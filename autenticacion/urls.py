from django.urls import path
from . views import VRegistro, VLogin, cuenta, eliminar_cuenta, favoritos
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('', VRegistro.as_view(), name='autenticacion'),
    #path("departamento/<int:id>/", views.departamento_informacion, name="departamento_informacion") 
    path("login/", VLogin.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("cuenta/", view=cuenta,name='cuenta'),
    path("favoritos/", view=favoritos, name="favoritos"),
    
        path('cambiar-contraseña/', auth_views.PasswordChangeView.as_view(
        template_name='cambiar_contrasena.html',  # tu template
        success_url=reverse_lazy('cuenta')  # redirige a la página de cuenta después de cambiar
    ), name='cambiar_contrasena'),
    
    #eliminar cuenta
    path('eliminar-cuenta/', eliminar_cuenta, name='eliminar_cuenta')
]

