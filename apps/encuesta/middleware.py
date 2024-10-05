# from django.shortcuts import redirect
# import re

# class BlockSpecificRoutesMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Expresiones regulares para las rutas que deseas bloquear
#         blocked_patterns = [
#             r'^/encuesta/',  # Bloquea todas las rutas que comienzan con /encuesta/
#             r'^/usuario/',   # Bloquea todas las rutas que comienzan con /usuario/
#         ]
        
#         for pattern in blocked_patterns:
#             if re.match(pattern, request.path):
#                 return redirect('index')  # Redirigir a la vista principal o donde desees
        
#         response = self.get_response(request)
#         return response
