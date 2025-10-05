from django.shortcuts import render
from .models import Departamentos, ImagenDepartamento
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import FormularioDepartamento
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Departamentos, ImagenDepartamento
from django.contrib.contenttypes.models import ContentType
from usuarios.models import Favorito
from django.utils.dateparse import parse_date
from django.http import HttpResponseForbidden
# Create your views here.



# departamentos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from usuarios.models import Comentario
from usuarios.forms import ComentarioForm
from .models import Departamentos

def departamento_informacion(request, id):
    
    departamento = get_object_or_404(Departamentos, id=id)
    tipo = ContentType.objects.get_for_model(Departamentos)

    en_favoritos = False
    if request.user.is_authenticated:
        en_favoritos = Favorito.objects.filter(
            usuario=request.user,
            content_type=tipo,
            object_id=departamento.id
        ).exists()

    comentarios_list = Comentario.objects.filter(content_type=tipo, object_id=departamento.id).order_by('-creado')

    #PAGINADOR
    paginator = Paginator(comentarios_list, 5)
    page_number = request.GET.get('page')
    comentarios = paginator.get_page(page_number)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.content_type = tipo
            comentario.object_id = departamento.id

            #respuestas
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comentario.parent_id = parent_id
            comentario.save()
            return redirect('departamentos_informacion', id=id)
    if request.method == "POST":
        if "favorito" in request.POST:
        # ✔ Checkbox marcado → crear favorito
         Favorito.objects.get_or_create(
            usuario=request.user,
            content_type=tipo,
            object_id=departamento.id
            )
        else:
            # ❌ Checkbox desmarcado → borrar favorito
            Favorito.objects.filter(
                usuario=request.user,
                content_type=tipo,
                object_id=departamento.id
            ).delete()
        return redirect("departamentos_informacion", id=id)
    else:
        form = ComentarioForm()

    return render(request, "departamento_informacion.html", {
        "departamento": departamento,
        "comentarios": comentarios,
        "form": form,
        "en_favoritos": en_favoritos
    })



def alquileres(request):
    departamentos = Departamentos.objects.filter(aprobado=True)

   



    precio_max = request.GET.get('precio_max')
    habitaciones = request.GET.get('habitaciones')
    banos = request.GET.get('banos')
    disponibles = request.GET.get('disponibles') #checkbox ON o none
    zona = request.GET.get('zona')
    moneda = request.GET.get('moneda')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')

    if precio_max:
        departamentos = departamentos.filter(precio__lte=precio_max)

    if moneda:
        departamentos = departamentos.filter(monedas=moneda)
    
    if habitaciones:
        departamentos = departamentos.filter(habitaciones=habitaciones)

    if banos:
        departamentos = departamentos.filter(banos=banos)

    if disponibles == 'on':
        departamentos = departamentos.filter(disponibilidad=True)

    
    if zona:
        departamentos = departamentos.filter(zona__icontains=zona)

    if fecha_desde:
        departamentos = departamentos.filter(fecha_publicacion__date__gte=parse_date(fecha_desde))
    if fecha_hasta:
        departamentos = departamentos.filter(fecha_publicacion__date__lte=parse_date(fecha_hasta))

    paginator = Paginator(departamentos, 8)  # Mostrar 6 departamentos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    return render(request, "departamentos.html", {"departamentos": page_obj, "page_obj": page_obj})

@login_required
def publicar_departamento(request):
    if request.user.tipo != 'propietario' or 'departamento' not in request.user.tipo_publicacion:
        return HttpResponseForbidden()
        
    
    if request.method == 'POST':
        form = FormularioDepartamento(request.POST, request.FILES)
        if form.is_valid():
            departamento = form.save(commit=False)
            departamento.propietario = request.user
            departamento.aprobado = False
            messages.success(request, "Su publicación se ha realizado con éxito. En estos momentos se encuentra en estado PENDIENTE a la espera de ser aceptada.")
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
     departamento = get_object_or_404(Departamentos,id=id)
     if departamento:
            departamento.delete()
            messages.success(request,"Departamento eliminado correctamente.")
            return redirect('departamentos')
     else:
            return redirect('departamentos')
     return redirect('departamentos')


#def editarcomentario(request, id):
 #   comentario = get_object_or_404(Comentario,id=id)
  #  if request.method == 'POST':
   #     form = ComentarioForm(request.POST, instance=comentario)
    #    if form.is_valid():
     #       form.save()
      #      messages.success(request, "Comentario editado correctamente.")
       #     return redirect("departamento_informacion", id=comentario.object_id)
    #else:
     #   form = ComentarioForm(instance=comentario)

   # return render(request, "editar_comentario.html", {"form": form, "comentario": comentario})
    