ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-alpine3.18 AS base

# Install only essential runtime dependencies
RUN apk add --no-cache \
    firefox-esr \
    chromium \
    chromium-chromedriver

FROM base AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

# Install build dependencies and compile packages
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    linux-headers

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Compile Python files and remove source code
COPY . .
RUN python -m compileall -b . && \
    find . -type f -name "*.py" ! -name "requirements.txt" -delete && \
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

FROM base AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DOCKERIZED=true
WORKDIR /app

# Install only essential runtime dependencies for final stage
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    linux-headers \
    && pip install --no-cache-dir \
    flask==3.1.1 \
    gunicorn==23.0.0 \
    selenium==4.35.0 \
    webdriver-manager==4.0.2 \
    python-dotenv==1.1.1 \
    psutil==7.0.0 \
    requests==2.32.5 \
    screeninfo==0.8.1 \
    && apk del .build-deps

COPY --from=builder /app .

EXPOSE 3000

ENTRYPOINT ["gunicorn", "-w", "2", "-b", "0.0.0.0:3000", "--timeout", "600", "main:app"]