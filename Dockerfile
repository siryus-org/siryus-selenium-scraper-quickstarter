# Use a light python image
ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base

# Avoid the creation of PyC files and bufferized output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define the Labor Directory
WORKDIR /app

# Copy and download dependencies before the source code (for efficient cache)
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --no-cache-dir -r requirements.txt

# Install necessary dependencies
RUN apt-get update && apt-get install -y wget \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && apt-get install -y firefox-esr
    && apt-get clean


# Create a non-root user for safety
USER root

# Copy the source code after installing units
COPY . .

# Exposes the port of Gunicorn (default 8000)
EXPOSE 8000

# Gunicorn executes with 4 worlds in production mode
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
