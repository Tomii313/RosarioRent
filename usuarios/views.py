from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.contenttypes.models import ContentType
from .models import Comentario
from salones.models import salones
from departamentos.models import Departamentos
from oficinas.models import Oficina
from .forms import ComentarioForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render

def departamento_informacion(request, id):
    departamento = get_object_or_404(Departamentos, id=id)
    comentarios = Comentario.objects.filter(departamento=departamento)

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.departamento = departamento  # relacion directa
            comentario.save()
            return redirect('departamento_informacion', id=id)
    else:
        form = ComentarioForm()

    return render(request, "departamento_informacion.html", {
        "departamento": departamento,
        "comentarios": comentarios,
        "form": form,
    })


def toggle_favorito(request, modelo, id):
    if not request.user.is_authenticated:
        return redirect('login')

    #diccionario que traduce el string modelo a la clase de modelo real

    modelo_class = {
        "departamento": Departamento,
        "oficina": Oficina,
        "salon": salones
    }.get(modelo)

    #obtengo el objeto real: ej oficina con id 3

    objeto = get_object_or_404(modelo_class, id=id)


      # obtengo el tipo de modelo (ContentType)
    content_type = ContentType.objects.get_for_model(modelo_class)

    # intento crear el favorito (si ya existe, no lo crea)
    favorito, creado = Favorito.objects.get_or_create(
        usuario=request.user,
        content_type=content_type,
        object_id=objeto.id
    )

    if not creado:  
        favorito.delete()  
        # si ya existía el favorito, lo borro (toggle: quita/añade)

    # redirijo a la página de detalle de donde estaba
    return redirect(f"{modelo}s_informacion", id=id)


def mis_favoritos(request):
    favoritos = Favorito.objects.filter(usuario=request.user).order_by("-agregado")
    # todos los favoritos del usuario, los más nuevos primero
    return render(request, "mis_favoritos.html", {"favoritos": favoritos})

@login_required
def baneado(request):
    if not getattr(request.user, "baneado", False):
        return redirect("home")
    return render(request, "baneado.html")



def editar_comentario(request, id):
    comentario = get_object_or_404(Comentario, id=id, usuario=request.user)
    modelo = comentario.content_type.model  # "departamentos", "oficinas", "salones"
    url_name = f"{modelo}_informacion"

    if request.method == "POST":
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()

            # dinámico: resuelve la URL según el tipo de publicación
          
            return redirect(url_name, comentario.object_id)
    else:
        form = ComentarioForm(instance=comentario)

    return render(request, "editar_comentario.html", {
        "form": form,
        "comentario": comentario,
        "url_name": url_name, 
    })


def eliminar_comentario(request,id):
    
    comentario = get_object_or_404(Comentario, id=id, usuario=request.user)
    modelo = comentario.content_type.model  # "departamentos", "oficinas", "salones"
    url_name = f"{modelo}_informacion"

    if request.method == 'POST':
     if comentario:
        comentario.delete()
        return redirect(url_name, comentario.object_id)
    return render(request, "home.html", {
        "comentario": comentario,
        "url_name": url_name, 
    })



    
#def terminos():
    