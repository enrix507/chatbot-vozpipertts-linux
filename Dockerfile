FROM python:3.9-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libespeak-ng1 \
    espeak-ng-espeak \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt .
COPY chatbot.py .
COPY chat_test.html .
COPY piper/ ./piper/

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Dar permisos de ejecución a los binarios de Piper
RUN chmod +x /app/piper/piper /app/piper/piper_phonemize

# Exponer el puerto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "chatbot.py"]
