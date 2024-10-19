# Usa una imagen base de Python
FROM python:3.9

# Establecer una variable de entorno
ENV APP_HOME /app

# Crear y establecer el directorio de trabajo
WORKDIR $APP_HOME

# Copia todos los archivos necesarios
COPY . ./ 

# Instalar las dependencias, incluyendo google-cloud-storage
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto que tu aplicación escuchará
EXPOSE 8080

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", ":$PORT", "--workers", "1", "--threads", "8", "--timeout", "0", "main:app"]
