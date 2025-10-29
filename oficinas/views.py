from django.shortcuts import render
from .models import Oficina, ImagenOficina
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from .forms import FormularioOficinas
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from usuarios.models import Comentario
from usuarios.forms import ComentarioForm
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from usuarios.models import Favorito
from django.utils.dateparse import parse_date
from django.http import HttpResponseForbidden
# Create your views here.

 #def oficinas_view(request):
 #   oficinas_list = Oficina.objects.filter(aprobado=True)
  #  return render(request, 'oficinas.html', {'oficinas': oficinas_list})


def alquileres(request):
    oficinas = Oficina.objects.filter(aprobado=True)

    precio_max = request.GET.get('precio_max')
    ambientes = request.GET.get('ambientes')
    disponibles = request.GET.get('disponibles') #checkbox ON o none
    zona = request.GET.get('zona')
    moneda = request.GET.get('moneda')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')

    if precio_max:
        oficinas = oficinas.filter(precio__lte=precio_max)

    if moneda:
        oficinas = oficinas.filter(monedas=moneda)
    
    if ambientes:
        oficinas = oficinas.filter(ambientes=ambientes)

    if disponibles == 'on':
        oficinas = oficinas.filter(disponible=True)

    if zona:
        oficinas = oficinas.filter(zona=zona)

    if fecha_desde:
        oficinas = oficinas.filter(fecha_publicacion__date__gte=parse_date(fecha_desde))
    if fecha_hasta:
        oficinas = oficinas.filter(fecha_publicacion__date__lte=parse_date(fecha_hasta))

    paginator = Paginator(oficinas, 8)  # Mostrar 6 departamentos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "oficinas.html", {"oficinas":page_obj, "page_obj":page_obj})


def oficinas_informacion(request, id):
    oficina_info = get_object_or_404(Oficina, id=id)
    oficina_type = ContentType.objects.get_for_model(Oficina)
   

    en_favoritos = False
    if request.user.is_authenticated:
        en_favoritos = Favorito.objects.filter(
            usuario=request.user,
            content_type=oficina_type,
            object_id=oficina_info.id
        ).exists()
    # Filtramos los comentarios de esa oficina
    comentarios_list = Comentario.objects.filter(
        content_type=oficina_type,
        object_id=oficina_info.id
    ).order_by('-creado')

    paginator = Paginator(comentarios_list, 5)
    page_number = request.GET.get('page')
    comentarios = paginator.get_page(page_number)
    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.content_type = oficina_type
            comentario.object_id = oficina_info.id
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comentario.parent_id = parent_id
            comentario.save()
            # 👇 El redirect ahora usa el nombre correcto de la URL
            return redirect("oficina_informacion", id=id)
    if request.method == "POST":
        if "favorito" in request.POST:
        # ✔ Checkbox marcado → crear favorito
         Favorito.objects.get_or_create(
            usuario=request.user,
            content_type=oficina_type,
            object_id=oficina_info.id
            )
        else:
            # ❌ Checkbox desmarcado → borrar favorito
            Favorito.objects.filter(
                usuario=request.user,
                content_type=oficina_type,
                object_id=oficina_info.id
            ).delete()
        return redirect("oficina_informacion", id=id)
    else:
        form = ComentarioForm()

    return render(request, "oficinas_informacion.html", {
    "oficina": oficina_info,
    "comentarios": comentarios,
    "form": form,
    "en_favoritos": en_favoritos
})

@login_required
def publicar_oficina(request):
    if request.user.tipo != 'propietario' or 'oficina' not in request.user.tipo_publicacion:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = FormularioOficinas(request.POST, request.FILES)
        if form.is_valid():
           
            oficina = form.save(commit=False)
            oficina.propietario = request.user
            oficina.aprobado = False
            messages.success(request, "Su publicación se ha realizado con éxito. En estos momentos se encuentra en estado PENDIENTE a la espera de ser aceptada.")
            oficina.save()

            for imagen in request.FILES.getlist('imagenes'):
                ImagenOficina.objects.create(oficina=oficina, imagen=imagen)
            return redirect('oficinas')
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
            <p>Detalle de la publicación: <strong>{publicacion.direccion}</strong></p>
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


def eliminarpublicacion(request,id):
    message=None
    
    if request.method == 'POST':
     oficina = get_object_or_404(Oficina,id=id)
     if oficina:
            oficina.delete()
            messages.success(request,"Oficina eliminada correctamente.")
            return redirect('oficinas')
     else:
            return redirect('oficinas')
     return redirect('oficinas')


