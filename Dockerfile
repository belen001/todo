# Usar una imagen oficial ligera de Python
FROM python:3.11-slim

# Evitar que Python escriba archivos .pyc en el contenedor
ENV PYTHONDONTWRITEBYTECODE=1
# Evitar que Python almacene en búfer las salidas de log (salida inmediata a consola)
ENV PYTHONUNBUFFERED=1

# Configurar el directorio de trabajo
WORKDIR /app

# Instalar dependencias antes de copiar el código para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto al contenedor
COPY main.py .
COPY templates/ templates/

# Crear un usuario no privilegiado para ejecutar la aplicación (seguridad)
RUN useradd -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Exponer el puerto por defecto de Flask
EXPOSE 5000

# Comando por defecto para producción usando Gunicorn como servidor WSGI
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
