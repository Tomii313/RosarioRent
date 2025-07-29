from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages

# Create your views here.
def home_view(request):
    return render(request,"home.html")


def contacto(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        email = request.POST.get("email")
        telefono = request.POST.get("telefono")
        mensaje = request.POST.get("mensaje")

        html_content = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #2c3e50;">Nuevo mensaje desde RosarioRent</h2>
            <p><strong>Nombre:</strong> {nombre}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Teléfono:</strong> {telefono}</p>
            <p><strong>Mensaje:</strong><br>{mensaje}</p>
            <img src="https://i.imgur.com/IOcX6HL.png" alt="RosarioRent Logo" style="width: 150px; height: auto; margin-top: 20px; border-radius: 8px;">
        </div>
        """

        email_msg = EmailMessage(
            subject="Nuevo mensaje desde RosarioRent",
            body=html_content,
            from_email=settings.EMAIL_HOST_USER,
            to=["tomidiazmoreno@gmail.com"],
        )
        email_msg.content_subtype = "html"  # Importante: dice que el cuerpo es HTML
        email_msg.send()



        messages.success(request, "¡Mensaje enviado correctamente! Pronto nos estaremos contactando." )
        return redirect('home')
    return redirect('home')