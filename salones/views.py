from django.shortcuts import render
from .models import salones, ImagenSalon



def salones_view(request):
    salones_list = salones.objects.all()
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
