@echo off

:: Guarda la ruta actual (donde se ejecuta el script)
set "PROJECT_DIR=%~dp0"

:: Abre Visual Studio Code en la carpeta del proyecto (opcional)
start code "%PROJECT_DIR%"

:: Ejecuta el servidor Django en el puerto 4000
python manage.py runserver 4000

pause
