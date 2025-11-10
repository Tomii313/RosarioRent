from django.shortcuts import render
from django.views.generic import View
from .forms import FormularioRegistro, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from usuarios.models import Favorito
from django.core.paginator import Paginator
from departamentos.models import Departamentos
from oficinas.models import Oficina
from salones.models import salones
from django.core.paginator import Paginator
from itertools import chain
from allauth.socialaccount.signals import social_account_added
from django.dispatch import receiver
from allauth.account.signals import user_signed_up


class VRegistro(View):
    def get(self, request):
          form = FormularioRegistro()
          return render(request, 'autenticacion.html', {'form': form})        
    
    def post(self,request):
            form = FormularioRegistro(request.POST)
            if form.is_valid():
                 user = form.save()
                 raw_password = form.cleaned_data.get('password1')  # asumiendo que usás UserCreationForm
                 user = authenticate(request, email=user.email, password=raw_password)
                 if user is not None:
                  login(request, user)
                  return redirect('home')
            return render(request, 'autenticacion.html', {'form': form, 'mensaje': 'Error al crear el usuario'})

class VLogin(View):
      def get(self, request):
          form = AuthenticationForm()
          return render(request, 'login.html', {'form': form})        
    
      def post(self,request):
          form = AuthenticationForm(request, data=request.POST)
          if form.is_valid():
            login(request, form.get_user())
            return redirect('home')  # Cambiá 'home' por la vista que quieras mostrar después del login
          else:
            return render(request, 'login.html', {'form': form, 'mensaje': 'Credenciales inválidas'})
          





def cuenta(request):
    if request.method == 'POST' and 'avatar' in request.FILES:
        request.user.avatar = request.FILES['avatar']
        request.user.save()
        return redirect('cuenta')

    if 'eliminaravatar' in request.POST:
        request.user.avatar = 'avatars/default_avatar.png'
        request.user.save()
        return redirect('cuenta')
       
    departamentos = Departamentos.objects.filter(propietario=request.user)
    oficinas = Oficina.objects.filter(propietario=request.user)
    salon = salones.objects.filter(propietario=request.user)


    # Paginadores separados
    paginator_departamentos = Paginator(departamentos, 5)
    paginator_oficinas = Paginator(oficinas, 5)
    paginator_salones = Paginator(salon, 5)

    page_number_d = request.GET.get('page_d')
    page_number_o = request.GET.get('page_o')
    page_number_s = request.GET.get('page_s')

    page_obj_d = paginator_departamentos.get_page(page_number_d)
    page_obj_o = paginator_oficinas.get_page(page_number_o)
    page_obj_s = paginator_salones.get_page(page_number_s)

    return render(request, 'cuenta.html', {
        'user': request.user,
        'page_obj_d': page_obj_d,
        'page_obj_o': page_obj_o,
        'page_obj_s': page_obj_s
    })
@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('login')
    return render(request, 'confirmar_eliminar.html')
                

@login_required
def favoritos(request):
    favoritos_list = Favorito.objects.filter(usuario=request.user)
    paginator = Paginator(favoritos_list, 5)
    page_number = request.GET.get('page')
    favoritos = paginator.get_page(page_number)
    return render(request, "favoritos.html", {"favoritos":favoritos})


@receiver(social_account_added)
def completar_datos_social(sender, request, sociallogin, **kwargs):
    user = sociallogin.user

    #Nombre desde Gugul
    if not user.first_name and 'first_name' in sociallogin.account.extra_data:
        user.first_name = sociallogin.account.extra_data.get('given_name', '')

    if not user.last_name and 'family_name' in sociallogin.account.extra_data:
        user.last_name = sociallogin.account.extra_data.get('family_name', '')

    #Email

    if not user.email and 'email' in sociallogin.account.extra_data:
        user.email = sociallogin.account.extra_data.get('email')

    if not user.username:
        user.username = user.first_name or user.email.split('@')[0]

    if not user.nombre:
        user.nombre = user.first_name or 'Anónimo'

    user.save()


@receiver(user_signed_up)
def completar_datos_google(request, user, **kwargs):
    if not user.nombre:
        user.nombre = user.first_name or "Anónimo"
    if not user.apellido:
        user.apellido = user.last_name or ""
    user.save()
