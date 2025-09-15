from django.shortcuts import render
from .models import salones, ImagenSalon
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .forms import FormularioSalones
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from usuarios.models import Comentario
from usuarios.forms import ComentarioForm
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from usuarios.models import Favorito

# Create your views here.



def salones_view(request):
    salones_list = salones.objects.filter(aprobado=True)
    return render(request, "salones.html", {"salones":salones_list})

@login_required
def salones_informacion(request, id):
    salonesinfo = salones.objects.get(id=id)
    salones_type = ContentType.objects.get_for_model(salones)

    en_favoritos = False
    if request.user.is_authenticated:
        en_favoritos = Favorito.objects.filter(
            usuario=request.user,
            content_type=salones_type,
            object_id=salonesinfo.id
        ).exists()

    # Comentarios de ese salón
    comentarios_list = Comentario.objects.filter(
        content_type=salones_type,
        object_id=salonesinfo.id
    ).order_by('-creado')

    paginator = Paginator(comentarios_list, 5)
    page_number = request.GET.get('page')
    comentarios = paginator.get_page(page_number)

    form = ComentarioForm()

    if request.method == "POST":
        # Si es comentario
        if "texto" in request.POST:  # nombre del campo del form
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.usuario = request.user
                comentario.content_type = salones_type
                comentario.object_id = salonesinfo.id
                comentario.save()
                return redirect("salones_informacion", id=id)

        # Si es toggle de favoritos
        elif "favorito" in request.POST:
            Favorito.objects.get_or_create(
                usuario=request.user,
                content_type=salones_type,
                object_id=salonesinfo.id
            )
            return redirect("salones_informacion", id=id)
        else:
            Favorito.objects.filter(
                usuario=request.user,
                content_type=salones_type,
                object_id=salonesinfo.id
            ).delete()
            return redirect("salones_informacion", id=id)

    return render(request, "salones_informacion.html", {
        "salon": salonesinfo,
        "comentarios": comentarios,
        "form": form,
        "en_favoritos": en_favoritos
    })
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
