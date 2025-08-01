#!/bin/bash

echo "Iniciando servidor de produccion para PDF Downloader..."

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
    mkdir downloads
fi

# Crear directorio temporal si no existe
if [ ! -d "temp" ]; then
    echo "Creando directorio temporal..."
    mkdir temp
fi

# Iniciar el servidor de producción
echo "Iniciando servidor de produccion en http://127.0.0.1:5000"
python run_production.py

# El entorno virtual se desactivará automáticamente cuando se cierre el script
deactivate