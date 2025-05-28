# Use a light python image para build
ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-cache-dir -r requirements.txt

# Instala dependencias del sistema necesarias para compilar y ejecutar
RUN apt-get update && apt-get install -y wget \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && apt-get install -y firefox-esr \
    && apt-get clean

# Copia el código fuente
COPY . .

# Compila todo el código Python a bytecode (.pyc)
RUN python -m compileall -b .

# Elimina todos los archivos fuente .py (excepto requirements.txt y recursos necesarios)
RUN find . -type f -name "*.py" ! -name "requirements.txt" -delete

# --- Imagen final ---
FROM python:${PYTHON_VERSION}-slim as final
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY --from=builder /app/requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-cache-dir -r requirements.txt

# Instala solo las dependencias del sistema necesarias para ejecutar
RUN apt-get update && apt-get install -y wget \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && apt-get install -y firefox-esr \
    && apt-get clean

# Copia solo los archivos compilados y recursos necesarios
COPY --from=builder /app .

# Exponer el puerto
EXPOSE 3000

# Ejecutar Gunicorn apuntando al módulo principal (main:app)
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:3000", "--timeout", "600", "main:app"]