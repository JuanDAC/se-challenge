# Usa una imagen base de Python
FROM python:3.12-slim-buster

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de requerimientos
COPY requirements.txt /app/requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia el código de la aplicación
COPY ./app /app

# Expone el puerto en el que la aplicación escuchará
EXPOSE 8000

# Define el comando para ejecutar la aplicación
CMD ["uvicorn", "app.presentation.http.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

