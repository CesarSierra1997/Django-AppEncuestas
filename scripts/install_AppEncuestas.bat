@echo off

:: Función para descargar Python
:download_python
echo Descargando instalador de Python...
curl -o python-installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe
if %errorlevel% neq 0 (
    echo Error al descargar el instalador de Python.
    pause
    exit /b
)
echo Instalador descargado con éxito.
goto :install_python

:: Función para instalar Python
:install_python
echo Instalando Python...
python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
if %errorlevel% neq 0 (
    echo Error al instalar Python.
    pause
    exit /b
)
echo Python instalado con éxito.
del python-installer.exe
goto :install_requirements

:: Verifica si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python no está instalado. Procediendo a instalarlo...
    goto :download_python
)

:install_requirements
:: Instala las dependencias desde requirements.txt
echo Instalando dependencias...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error al instalar las dependencias.
    pause
    exit /b
)

echo Instalación completada.
pause
