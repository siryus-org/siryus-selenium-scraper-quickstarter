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

# Copy application source (keep .py files for tests)
COPY . .

FROM base AS final

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DOCKERIZED=true
WORKDIR /app

# Install only essential runtime dependencies for final stage
COPY requirements.txt .
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    linux-headers \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY --from=builder /app .

# Copy test sources so pytest can run inside the container
COPY test ./test

EXPOSE 3000

ENTRYPOINT ["gunicorn", "-w", "2", "-b", "0.0.0.0:3000", "--timeout", "600", "main:app"]