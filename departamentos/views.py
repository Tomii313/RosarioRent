from django.shortcuts import render
from .models import Departamentos, ImagenDepartamento
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import FormularioDepartamento
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Departamentos, ImagenDepartamento

# Create your views here.
def alquileres(request):
    departamentos = Departamentos.objects.all()
    return render(request, "departamentos.html", {"departamentos": departamentos})


def departamento_informacion(request, id):
    departamentos = Departamentos.objects.get(id=id)
    return render(request, "departamento_informacion.html", {"departamento": departamentos})


def alquileres(request):
    departamentos = Departamentos.objects.all()

    precio_max = request.GET.get('precio_max')
    habitaciones = request.GET.get('habitaciones')
    banos = request.GET.get('banos')
    disponibles = request.GET.get('disponibles') #checkbox ON o none
    zona = request.GET.get('zona')

    if precio_max:
        departamentos = departamentos.filter(precio__lte=precio_max)
    
    if habitaciones:
        departamentos = departamentos.filter(habitaciones=habitaciones)

    if banos:
        departamentos = departamentos.filter(banos=banos)

    if disponibles == 'on':
        departamentos = departamentos.filter(disponibilidad=True)

    
    if zona:
        departamentos = departamentos.filter(zona__icontains=zona)
    
    return render(request, "departamentos.html", {"departamentos": departamentos})

@login_required
def publicar_departamento(request):
    if request.user.tipo != 'propietario':
        return redirect('home')
    
    if request.method == 'POST':
        form = FormularioDepartamento(request.POST, request.FILES)
        if form.is_valid():
            departamento = form.save(commit=False)
            departamento.propietario = request.user
            departamento.save()

            for imagen in request.FILES.getlist('imagenes'):
                ImagenDepartamento.objects.create(departamento=departamento, imagen=imagen)
            return redirect('home')
    else:
        form = FormularioDepartamento()

    return render(request, 'publicar_departamento.html', {'form': form})



def contactar_propietario(request, publicacion_id):
    if request.method == "POST":
        publicacion = get_object_or_404(Departamentos, id=publicacion_id)
        propietario = publicacion.propietario
        propietario_email = propietario.email

        if not propietario.email:
            messages.error(request, "El propietario no tiene un email registrado.")
            return redirect('home')
        
        usuario = request.user

        html_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Interés en tu propiedad</h2>
            <p><strong>{usuario.username}</strong> está interesado/a en tu propiedad publicada en RosarioRent.</p>
            <p>Podés responderle al correo: <strong>{usuario.email}</strong></p>
            <p>Detalle de la publicación: <strong>{publicacion.nombre}</strong></p>
            <img src="https://i.imgur.com/IOcX6HL.png" alt="RosarioRent" style="width: 150px; margin-top: 20px;" />
        </div>
        """

        email_msg = EmailMessage(
            subject="Nuevo interesado en tu propiedad - RosarioRent",
            body=html_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[propietario_email],
        )
        email_msg.content_subtype = "html"
        email_msg.send()

        messages.success(request, "¡El propietario ha sido notificado correctamente!")
        return redirect('home')

    return redirect('home')
