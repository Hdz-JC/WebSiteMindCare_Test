# Usamos Python 3.12 Slim (ligero)
FROM python:3.12-slim

# Evitamos archivos basura de python y logs en buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos dependencias del sistema necesarias para Postgres
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamos requirements e instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de la app
COPY . .

# Exponemos el puerto interno de Flask
EXPOSE 5000

# Arrancamos con Gunicorn escuchando en 0.0.0.0 (Todo internet)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]