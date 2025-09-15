from django.shortcuts import redirect
from django.urls import reverse

class CheckBanMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__ (self,request):
         if request.user.is_authenticated and getattr(request.user, "baneado", False):
            if not request.user.is_superuser and request.path != reverse("baneado"):  # evita loop
                return redirect("baneado")

         return self.get_response(request)