@echo off
echo Iniciando servidor de produccion para PDF Downloader...

:: Verificar si Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python no esta instalado o no esta en el PATH.
    echo Por favor, instale Python y asegurese de agregarlo al PATH.
    pause
    exit /b 1
)

:: Verificar si existe el entorno virtual, si no, crearlo
if not exist venv (
    echo Creando entorno virtual...
    python -m venv venv
)

:: Activar el entorno virtual
call venv\Scripts\activate.bat

:: Instalar dependencias
echo Instalando dependencias...
pip install -r requirements.txt

:: Crear directorio de descargas si no existe
if not exist downloads (
    echo Creando directorio de descargas...
    mkdir downloads
)

:: Crear directorio temporal si no existe
if not exist temp (
    echo Creando directorio temporal...
    mkdir temp
)

:: Iniciar el servidor de produccion
echo Iniciando servidor de produccion en http://127.0.0.1:5000
python run_production.py

:: Desactivar el entorno virtual cuando se cierre el servidor
call venv\Scripts\deactivate.bat