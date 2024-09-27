from apps.encuesta.views import obtener_direccion_ip

def direccion_ip(request):
    # Obtener la dirección IP del usuario
    ip_address = obtener_direccion_ip(request)
    # Devuelve un diccionario con la dirección IP
    return {'ip_address': ip_address}
