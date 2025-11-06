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
from django.utils.dateparse import parse_date
from django.http import HttpResponseForbidden

# Create your views here.

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
    "Otro": (-32.95, -60.65),
}

def salones_view(request):
    salones_list = salones.objects.filter(aprobado=True)

    precio_max = request.GET.get('precio_max')
    capacidad = request.GET.get('capacidad')
    disponibles = request.GET.get('disponibles') #checkbox ON o none
    zona = request.GET.get('zona')
    moneda = request.GET.get('moneda')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')

    if precio_max:
        salones_list = salones_list.filter(precio__lte=precio_max)

    if moneda:
        salones_list = salones_list.filter(monedas=moneda)
    
    if capacidad:
        salones_list = salones_list.filter(capacidad=capacidad)

    if disponibles == 'on':
        salones_list = salones_list.filter(disponible=True)

    if zona:
        salones_list = salones_list.filter(zona=zona)
    if fecha_desde:
        salones_list = salones_list.filter(fecha_publicacion__date__gte=parse_date(fecha_desde))
    if fecha_hasta:
        salones_list = salones_list.filter(fecha_publicacion__date__lte=parse_date(fecha_hasta))

    paginator = Paginator(salones_list, 8)  # Mostrar 6 departamentos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

  
    return render(request, "salones.html", {"salones":page_obj, "page_obj":page_obj})


def salones_informacion(request, id):
    salon = get_object_or_404(salones, id=id)
    salon_type = ContentType.objects.get_for_model(salones)

    en_favoritos = False
    if request.user.is_authenticated:
        en_favoritos = Favorito.objects.filter(
            usuario=request.user,
            content_type=salon_type,
            object_id=salon.id
        ).exists()

    # Comentarios
    comentarios_list = Comentario.objects.filter(
        content_type=salon_type,
        object_id=salon.id
    ).order_by('-creado')

    paginator = Paginator(comentarios_list, 5)
    page_number = request.GET.get('page')
    comentarios = paginator.get_page(page_number)
    form = ComentarioForm()

    # --- POST: comentario o favorito ---
    if request.method == "POST":
        # Si es comentario
        if "texto" in request.POST:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.usuario = request.user
                comentario.content_type = salon_type
                comentario.object_id = salon.id
                parent_id = request.POST.get('parent_id')
                if parent_id:
                    comentario.parent_id = parent_id
                comentario.save()
                return redirect("salones_informacion", id=id)

        # Si es toggle de favoritos
        elif "favorito" in request.POST:
            Favorito.objects.get_or_create(
                usuario=request.user,
                content_type=salon_type,
                object_id=salon.id
            )
            return redirect("salones_informacion", id=id)

        # Si es eliminar de favoritos
        else:
            Favorito.objects.filter(
                usuario=request.user,
                content_type=salon_type,
                object_id=salon.id
            ).delete()
            return redirect("salones_informacion", id=id)

    # --- Cálculo de coordenadas ---
    delta = 0.01

    if salon.latitud and salon.longitud:
        lat = float(salon.latitud)
        lon = float(salon.longitud)
    elif salon.zona in ZONAS_COORDS:
        lat, lon = ZONAS_COORDS[salon.zona]
    else:
        lat = lon = None

    if lat and lon:
        lat_min = lat - delta
        lat_max = lat + delta
        lon_min = lon - delta
        lon_max = lon + delta

        # asegurar formato correcto
        lat = str(lat).replace(',', '.')
        lon = str(lon).replace(',', '.')
        lat_min = str(lat_min).replace(',', '.')
        lat_max = str(lat_max).replace(',', '.')
        lon_min = str(lon_min).replace(',', '.')
        lon_max = str(lon_max).replace(',', '.')
    else:
        lat_min = lat_max = lon_min = lon_max = lat = lon = None

    # --- Render final (siempre al final y fuera del POST) ---
    return render(request, "salones_informacion.html", {
        "salon": salon,
        "comentarios": comentarios,
        "form": form,
        "en_favoritos": en_favoritos,
        "lat_min": lat_min,
        "lat_max": lat_max,
        "lon_min": lon_min,
        "lon_max": lon_max,
        "lat": lat,
        "lon": lon,
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
    if request.user.tipo != 'propietario' or "salon" not in request.user.tipo_publicacion:
        return HttpResponseForbidden()
    
    if request.method == 'POST':
        form = FormularioSalones(request.POST, request.FILES)
        if form.is_valid():
            salon = form.save(commit=False)
            salon.propietario = request.user
            salon.aprobado = False
            messages.success(request, "Su publicación se ha realizado con éxito. En estos momentos se encuentra en estado PENDIENTE a la espera de ser aceptada.")
            lat, lon = geocode(f"{salon.direccion}, {salon.zona}")
            salon.latitud = lat
            salon.longitud = lon
            salon.save()

            for imagen in request.FILES.getlist('imagenes'):
                ImagenSalon.objects.create(salon=salon, imagen=imagen)
            return redirect('salones')
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
     salon = get_object_or_404(salones,id=id)
     if salon:
            salon.delete()
            messages.success(request,"Salón eliminado correctamente.")
            return redirect('salones')
     else:
            return redirect('salones')
     return redirect('salones')


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