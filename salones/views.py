from django.shortcuts import render
from .models import salones, ImagenSalon


def salones_view(request):
    salones_list = salones.objects.all()
    return render(request, "salones.html", {"salones":salones_list})

