from django.shortcuts import render
from .models import Oficina, ImagenOficina
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .forms import FormularioOficinas
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
# Create your views here.

def oficinas_view(request):
    oficinas_list = Oficina.objects.all()
    return render(request, 'oficinas.html', {'oficinas': oficinas_list})


def oficinas_informacion(request, id):
    oficina_info = Oficina.objects.get(id=id)
    return render(request, 'oficinas_informacion.html', {'oficina': oficina_info})


@login_required
def publicar_oficina(request):
    if request.user.tipo != 'propietario':
        return redirect('home')
    
    if request.method == 'POST':
        form = FormularioOficinas(request.POST, request.FILES)
        if form.is_valid():
            oficina = form.save(commit=False)
            oficina.propietario = request.user
            oficina.save()

            for imagen in request.FILES.getlist('imagenes'):
                ImagenOficina.objects.create(oficina=oficina, imagen=imagen)
            return redirect('home')
    else:
        form = FormularioOficinas()

    return render(request, 'publicar_oficina.html', {'form': form})



def contactar_propietario(request, publicacion_id):
    if request.method == "POST":
        publicacion = get_object_or_404(Oficina, id=publicacion_id)
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

