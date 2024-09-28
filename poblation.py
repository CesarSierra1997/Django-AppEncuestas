import os
import django
import time
import random
from faker import Faker

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Encuesta.settings')  # Reemplaza 'tu_proyecto' con el nombre de tu proyecto
django.setup()

from apps.usuario.models import Usuario, Rol

fake = Faker()

def generate_usuario(num_users):
    for i in range(num_users):
        # Intenta obtener una instancia del rol
        try:
            # Cambia el número a uno que exista en tu base de datos
            rol_instance = Rol.objects.get(id=1)  # Reemplaza 1 con el ID que desees
        except Rol.DoesNotExist:
            print("El rol no existe. Asegúrate de tener roles en la base de datos.")
            continue  # Continúa con el siguiente usuario si el rol no existe

        # Crea un nuevo usuario
        Usuario.objects.create(
            username=f'usuario{i}',
            email=f'usuario{i}@ejemplo.com',
            password='contraseña_segura',  # Cambia esto para generar contraseñas seguras si es necesario
            rol=rol_instance,  # Asignar la instancia del rol
            nombres=fake.first_name(),
            apellidos=fake.last_name(),
            tipoDocumento='CC',  # Cambia según tus necesidades
            numeroDocumento=fake.random_int(min=1000000, max=99999999)
        )

if __name__ == "__main__":
    print("Iniciando la población de usuarios...")
    print("Por favor espere . . .")
    start = time.strftime("%c")
    print(f'Fecha y hora de inicio: {start}')
    generate_usuario(2000)  # Cambia la cantidad de usuarios que desees crear
    end = time.strftime("%c")
    print(f'Fecha y hora de finalización: {end}')

