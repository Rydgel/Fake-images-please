FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libwebp-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    zlib1g-dev \
    libfreetype6-dev \
    # Additional dependencies for Pillow
    libtiff5-dev \
    libxcb1-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --prefix=/install --no-cache-dir -r /tmp/requirements.txt

# --- Production Image ---
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy installed dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy the application code
COPY ./app /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo \
    libwebp7 \
    libfreetype6 \
    libtiff6 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Expose the port
EXPOSE 80

# Add a healthcheck (adjust the path as needed)
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl --fail http://localhost/check || exit 1

# Run Gunicorn (adjust the number of workers and other settings as needed)
CMD ["gunicorn", "--bind", "0.0.0.0:80", "--workers", "4", "main:app"]
