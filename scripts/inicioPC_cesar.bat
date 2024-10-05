@echo off
cd "c:/Users/cesar/OneDrive/Escritorio/Django/venv/Scripts"
call activate
cd "c:/Users/cesar/OneDrive/Escritorio/Django/Encuesta"

:: Abre Visual Studio Code en la carpeta del proyecto
start code .

:: Ejecuta el servidor Django
python manage.py runserver 4000
pause
