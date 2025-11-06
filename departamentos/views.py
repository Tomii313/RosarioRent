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
import requests
# Create your views here.



# departamentos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from usuarios.models import Comentario
from usuarios.forms import ComentarioForm
from .models import Departamentos



ZONAS_COORDS = {
    "Centro": (-32.949422, -60.643295),
    "Macrocentro": (-32.955, -60.648),
    "Echesortu": (-32.950, -60.680),
    "Abasto": (-32.931, -60.700),
    "Tablada": (-32.930, -60.630),
    "Las Delicias": (-33.000, -60.670),
    "Fisherton": (-32.930, -60.760),
    "Arroyito": (-32.915, -60.675),
    "Pichincha": (-32.942, -60.660),
    "Luis Agote": (-32.943, -60.676),
    "Alberdi": (-32.888, -60.698),
    "Empalme Graneros": (-32.910, -60.714),
    "Ludueña": (-32.950, -60.710),
    "Belgrano": (-32.965, -60.725),
    "Azcuénaga": (-32.955, -60.695),
    "Refinería": (-32.931, -60.624),
    "Hospitales": (-32.970, -60.640),
    "La Florida": (-32.874, -60.690),
    "Sarmiento": (-32.945, -60.635),
    "Hostal del Sol": (-32.995, -60.735),
    "Barrio Rucci": (-32.892, -60.674),
    "Godoy": (-32.967, -60.750),
    "7 de Septiembre": (-32.920, -60.725),
    "Lisandro de la Torre": (-32.885, -60.710),
    "Antártida Argentina": (-32.910, -60.740),
    "Lomas de Alberdi": (-32.880, -60.700),
    "Zona Norte": (-32.890, -60.700),
    "Zona Oeste": (-32.960, -60.740),
    "Zona Este": (-32.940, -60.620),
    "Zona Sur": (-33.000, -60.660),
    "Zona Suroeste": (-32.985, -60.720),
    "Zona Sudeste": (-33.000, -60.620),
    "Villa Gobernador Gálvez": (-33.020, -60.640),
    "Granadero Baigorria": (-32.854, -60.705),
    "San Lorenzo": (-32.747, -60.732),
    "Fray Luis Beltrán": (-32.784, -60.733),
    "Ricardone": (-32.754, -60.816),
    "Funes": (-32.916, -60.825),
    "Roldán": (-32.898, -60.904),
    "Soldini": (-33.014, -60.775),
    "Perez": (-32.983, -60.785),
    "Puente Gallego": (-33.027058, -60.685670),
    
}
def departamento_informacion(request, id):
    departamento = get_object_or_404(Departamentos, id=id)
    tipo = ContentType.objects.get_for_model(Departamentos)

    # Ver si está en favoritos
    en_favoritos = False
    if request.user.is_authenticated:
        en_favoritos = Favorito.objects.filter(
            usuario=request.user,
            content_type=tipo,
            object_id=departamento.id
        ).exists()

    # Comentarios
    comentarios_list = Comentario.objects.filter(
        content_type=tipo, 
        object_id=departamento.id
    ).order_by('-creado')
    paginator = Paginator(comentarios_list, 5)
    page_number = request.GET.get('page')
    comentarios = paginator.get_page(page_number)

    # Comentario form
    if request.method == 'POST' and 'texto' in request.POST:
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.content_type = tipo
            comentario.object_id = departamento.id

            # respuestas
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comentario.parent_id = parent_id
            comentario.save()
            return redirect('departamentos_informacion', id=id)
    else:
        form = ComentarioForm()

    # Checkbox favoritos
    if request.method == "POST" and "favorito" in request.POST:
        Favorito.objects.get_or_create(
            usuario=request.user,
            content_type=tipo,
            object_id=departamento.id
        )
        return redirect("departamentos_informacion", id=id)
    elif request.method == "POST":
        Favorito.objects.filter(
            usuario=request.user,
            content_type=tipo,
            object_id=departamento.id
        ).delete()
        return redirect("departamentos_informacion", id=id)

    # --- NUEVO: calcular límites del mapa ---
    delta = 0.01

    if departamento.latitud and departamento.longitud:
        lat = float(departamento.latitud)
        lon = float(departamento.longitud)
    elif departamento.zona in ZONAS_COORDS:
        lat, lon = ZONAS_COORDS[departamento.zona]
    else:
        lat = lon = None

    if lat and lon:
        # calculamos los límites primero
        lat_min = lat - delta
        lat_max = lat + delta
        lon_min = lon - delta
        lon_max = lon + delta

        # y luego forzamos que siempre se usen puntos
        lat = str(lat).replace(',', '.')
        lon = str(lon).replace(',', '.')
        lat_min = str(lat_min).replace(',', '.')
        lat_max = str(lat_max).replace(',', '.')
        lon_min = str(lon_min).replace(',', '.')
        lon_max = str(lon_max).replace(',', '.')
    else:
        lat_min = lat_max = lon_min = lon_max = lat = lon = None

    return render(request, "departamento_informacion.html", {
        "departamento": departamento,
        "comentarios": comentarios,
        "form": form,
        "en_favoritos": en_favoritos,
        # nuevos contextos para el mapa
        "lat_min": lat_min,
        "lat_max": lat_max,
        "lon_min": lon_min,
        "lon_max": lon_max,
        "lat": lat,
        "lon": lon,
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
            departamento.save()

            # obtener latitud y longitud
            lat, lon = geocode(f"{departamento.direccion}, {departamento.zona}")
            departamento.latitud = lat
            departamento.longitud = lon
            departamento.save()

            for imagen in request.FILES.getlist('imagenes'):
                ImagenDepartamento.objects.create(departamento=departamento, imagen=imagen)
            
            messages.success(request, "Su publicación se ha realizado con éxito. En estos momentos se encuentra en estado PENDIENTE a la espera de ser aceptada.")
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
    
def geocode(direccion, zona=None, ciudad="Rosario", pais="Argentina"):
    """
    Devuelve latitud y longitud usando Nominatim.
    Combina dirección, zona, ciudad y país para aumentar la precisión.
    """
    import requests

    query = direccion
    if zona:
        query += f", {zona}"
    query += f", {ciudad}, {pais}"

    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "limit": 1
    }
    headers = {"User-Agent": "RosarioRentApp"}  # obligatorio
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print("Error geocoding:", e)

    # fallback si no encuentra nada
    return None, None