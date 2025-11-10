from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def home_view(request):
    request.session['estado'] = None
    mensajeinicial = "Hola 👋<br>Seleccioná una opción:<br>1. Acerca de Publicar<br>2. Acerca de Alquilar<br>3. Soporte"
    return render(request,"home.html", {"mensajeinicial": mensajeinicial})

    
def terminos(request):
    return render(request, "terminos.html")

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



def chatbot(request):

    if request.method == "POST":
        user_message = request.POST.get("message", "").strip().lower()
        estado = request.session.get("estado", None) #recuperamos el estado actual de la sesion
        if user_message == "1" and estado is None: #guardamos que ahora estamos en la sub_pregunta de la opcion 1
            request.session["estado"] = "publicar_pregunta"
            response = "Para publicar alguna propiedad debe registrarse como Propietario.\n Paso seguido, ir a la pantalla de 'Alquileres' y en dicha categoría en la que se registró, le aparecerá un botón verde que dice 'Publicar ...., donde será redirigido al formulario.\n Al finalizar el relleno del formulario, un administrador verá su solicitud y analizará si está apta para ser mostrada en RosarioRent.\nEsta es una plataforma totalmente gratuita que facilita el contacto entre propietarios e inquilinos, dejando en sus manos el acuerdo final y las condiciones de cada alquiler.\nTe resultó útil esta información?<br>1.Sí<br>2.No<br>3.Volver"
        
        elif user_message == "2" and estado is None:
             request.session["estado"] = "alquilar_pregunta"
             response = "Para alquilar un departamento, un salón o una oficina, debe entrar a la publicación y seleccionar la opción para contactar al propietario, dicha opción APARECERÁ SOLO SI USTED SE ENCUENTRA LOGEADO, puede contactarse mediante Correo o Whatsapp. Si desea guardar la publicación para consultar más adelante, puede hacer click en 'Añadir a Favoritos' y esta quedará guardada en la sección de 'Favoritos' que aparece al hacer click en su cuenta. Usted es libre de hacer comentarios públicamente en las publicaciones siempre cuando respete las normas y sean en el mismo contexto, en caso de que el usuario haga lo contrario su cuenta puede quedar suspendida de manera permanente. Recordemos que RosarioRent es únicamente una plataforma intermediaria para que usted y el propietario puedan ponerse en contacto. RosarioRent no participa en las transacciones ni garantiza la veracidad de la información publicada. En caso de detectar conductas sospechosas o haber sido víctima de una estafa, le recomendamos suspender la operación y denunciar inmediatamente al administrador de la plataforma y a las autoridades correspondientes.<br><br>3.Volver"

        elif user_message == "3" and estado is None:
            # Soporte
            response = "Para soporte, escribinos a soporte@rentarg.com"
            request.session["estado"] = None
        

        elif estado == "publicar_pregunta" and user_message == "1":
                response = "Nos alegramos que te haya sido útil la información! Ante cualquier otra consulta puede contactarse con el soporte a RosarioRent@gmail.com"
                request.session["estado"] = None
        elif estado == "publicar_pregunta" and user_message == "2":
                response = "Lamentamos que nuestra respuesta no haya sido de utilidad. Para una respuesta más elaborada escríbenos a soporte@rentarg.com o rellena el formulario que se encuentra en la página principal.<br><br><br>3.Volver"
                
        
        elif estado == "publicar_pregunta" and user_message == "3":
                response = "Hola 👋<br>Seleccioná una opción:<br>1. Acerca de Publicar<br>2. Acerca de Alquilar<br>3. Soporte"
                request.session["estado"] = None
        
        elif estado == "alquilar_pregunta" and user_message == "3":
           response = "Hola 👋<br>Seleccioná una opción:<br>1. Acerca de Publicar<br>2. Acerca de Alquilar<br>3. Soporte"
           request.session["estado"] = None


        else:
            response = "No entendí esa opción. Escribí 1, 2 o 3."

        return JsonResponse({'response': response})

def error_404(request, exception):
    return render(request, '404.html', status=404)
        
