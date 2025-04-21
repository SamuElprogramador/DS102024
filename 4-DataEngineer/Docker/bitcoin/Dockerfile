FROM python:3.11-slim

WORKDIR /app

# Copiar archivos de proyecto
COPY . .

# Instalar dependencias con pip
RUN pip install -e .

# El comando por defecto ejecuta el scheduler
CMD ["python", "-m", "bitcoin_etl.scheduler"]
