from django.shortcuts import render
from .models import salones, ImagenSalon
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .forms import FormularioSalones
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages



def salones_view(request):
    salones_list = salones.objects.filter(aprobado=True)
    return render(request, "salones.html", {"salones":salones_list})

def salones_informacion(request,id):
    salonesinfo = salones.objects.get(id=id)
    return render(request, "salones_informacion.html", {"salon": salonesinfo})


def alquileres(request):
    salones_list = salones.objects.all()

    precio_max = request.GET.get('precio_max')
    disponibles = request.GET.get('disponibles')
    capacidad = request.GET.get('capacidad')

    if precio_max:
        try:
            precio_max = int(precio_max)
            salones_list = salones_list.filter(precio__lte=precio_max)
        except ValueError:
            pass

    if disponibles == 'on':
        salones_list = salones_list.filter(disponible=True)

    if capacidad:
        try:
            capacidad = int(capacidad)
            salones_list = salones_list.filter(capacidad__lte=capacidad)
        except ValueError:
            pass

    return render(request, "salones.html", {"salones": salones_list})


@login_required
def publicar_salones(request):
    if request.user.tipo != 'propietario':
        return redirect('home')
    
    if request.method == 'POST':
        form = FormularioSalones(request.POST, request.FILES)
        if form.is_valid():
            salon = form.save(commit=False)
            salon.propietario = request.user
            salon.aprobado = False
            salon.save()

            for imagen in request.FILES.getlist('imagenes'):
                ImagenSalon.objects.create(salon=salon, imagen=imagen)
            return redirect('home')
    else:
        form = FormularioSalones()

    return render(request, 'publicar_salon.html', {'form': form})



def contactar_propietario(request, publicacion_id):
    if request.method == "POST":
        publicacion = get_object_or_404(salones, id=publicacion_id)
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
