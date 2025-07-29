from django.shortcuts import render
from django.views.generic import View
from .forms import FormularioRegistro, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect


class VRegistro(View):
    def get(self, request):
          form = FormularioRegistro()
          return render(request, 'autenticacion.html', {'form': form})        
    
    def post(self,request):
            form = FormularioRegistro(request.POST)
            if form.is_valid():
                 user = form.save()
                 username = form.cleaned_data.get('username')
                 raw_password = form.cleaned_data.get('password1')  # asumiendo que usás UserCreationForm
                 user = authenticate(username=username, password=raw_password)
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
                