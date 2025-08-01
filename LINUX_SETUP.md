# Configuración en Linux

Este documento proporciona instrucciones para configurar y ejecutar el PDF Paper Downloader en un entorno Linux.

## Opciones de Ejecución

Hay varias formas de ejecutar la aplicación en Linux:

### 1. Ejecución Manual con Script

Puedes usar el script `start_linux_production.sh` para iniciar la aplicación:

```bash
# Dar permisos de ejecución al script
chmod +x start_linux_production.sh

# Ejecutar el script
./start_linux_production.sh
```

Este script:
- Verifica si Python está instalado
- Crea un entorno virtual si no existe
- Instala las dependencias
- Crea los directorios necesarios
- Inicia el servidor Gunicorn

### 2. Configuración como Servicio Systemd

Para ejecutar la aplicación como un servicio del sistema que se inicie automáticamente:

1. Copia los archivos del proyecto a `/opt/pdf-downloader/`:

```bash
sudo mkdir -p /opt/pdf-downloader
sudo cp -r * /opt/pdf-downloader/
```

2. Configura los permisos:

```bash
sudo chown -R www-data:www-data /opt/pdf-downloader
sudo chmod +x /opt/pdf-downloader/start_linux_production.sh
```

3. Crea el entorno virtual e instala las dependencias:

```bash
cd /opt/pdf-downloader
sudo -u www-data python3 -m venv venv
sudo -u www-data venv/bin/pip install -r requirements.txt
```

4. Copia el archivo de servicio a la ubicación de systemd:

```bash
sudo cp /opt/pdf-downloader/pdf-downloader.service /etc/systemd/system/
```

5. Habilita e inicia el servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl enable pdf-downloader.service
sudo systemctl start pdf-downloader.service
```

6. Verifica el estado del servicio:

```bash
sudo systemctl status pdf-downloader.service
```

## Verificación

Para verificar que la aplicación está funcionando correctamente, puedes hacer una solicitud al endpoint de salud:

```bash
curl http://localhost:5000/health
```

Deberías recibir una respuesta JSON indicando que la API está funcionando.

## Solución de Problemas

Si encuentras problemas, puedes revisar los logs del servicio:

```bash
sudo journalctl -u pdf-downloader.service
```

O si estás ejecutando manualmente, los errores se mostrarán en la consola.

## Notas Adicionales

- La aplicación se ejecuta en el puerto 5000 por defecto. Si necesitas cambiar esto, puedes modificar el archivo de servicio o el script de inicio.
- Si estás detrás de un proxy inverso como Nginx o Apache, asegúrate de configurar correctamente el reenvío de solicitudes al puerto 5000.