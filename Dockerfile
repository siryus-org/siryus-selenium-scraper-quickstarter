ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim AS base

# Install runtime dependencies for browsers and rendering (Chrome/Firefox, fonts, gfx libs)
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    firefox-esr \
    chromium \
    chromium-driver \
    fonts-dejavu \
    fonts-liberation \
    fonts-freefont-ttf \
    libnss3 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxdamage1 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

FROM base AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

# Install build dependencies and compile packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Compile Python files and remove source code
COPY . .
RUN python -m compileall -b . && \
    find . -type f -name "*.py" -delete && \
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

FROM base AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DOCKERIZED=true \
    HOME=/home/scraper
WORKDIR /app

RUN groupadd --system scraper \
    && useradd --system --create-home --gid scraper --home-dir /home/scraper scraper

# Copy requirements and install dependencies
COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    && pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential gcc libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app .

RUN mkdir -p /app/logs /app/temp_downloads /tmp/prometheus-multiproc \
    && chown -R scraper:scraper /app/logs /app/temp_downloads /tmp/prometheus-multiproc \
    && chmod +x /app/docker-entrypoint.sh

USER scraper

EXPOSE 3000 9090

ENTRYPOINT ["/app/docker-entrypoint.sh"]
