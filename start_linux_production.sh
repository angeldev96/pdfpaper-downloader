#!/bin/bash

echo "Iniciando servidor de produccion para PDF Downloader en Linux..."

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado."
    echo "Por favor, instale Python 3 y vuelva a intentarlo."
    exit 1
fi

# Verificar si existe el entorno virtual, si no, crearlo
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar el entorno virtual
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Crear directorio de descargas si no existe
if [ ! -d "downloads" ]; then
    echo "Creando directorio de descargas..."
    mkdir -p downloads
    chmod 755 downloads
fi

# Crear directorio temporal si no existe
if [ ! -d "temp" ]; then
    echo "Creando directorio temporal..."
    mkdir -p temp
    chmod 755 temp
fi

# Iniciar el servidor de producción con Gunicorn
echo "Iniciando servidor Gunicorn en http://0.0.0.0:5000"

# Ejecutar Gunicorn con 4 workers, vinculado a todas las interfaces en el puerto 5000
exec gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:app

# Nota: El script no llegará a este punto debido al 'exec' anterior
# que reemplaza el proceso actual con Gunicorn
deactivate