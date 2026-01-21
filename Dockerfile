# Base image: lightweight Python
FROM python:3.12-slim

# Prevent Python from writing pyc files and enable logs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# System dependencies required by rasterio / pyproj / GDAL
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin \
    libgdal-dev \
    proj-bin \
    libproj-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy the application code
COPY . /app

# Expose FastAPI port
EXPOSE 8000

# Default dataset path (can be overridden)
ENV DATA_PATH=/app/data/geographic_data/GHS_POP_E2030_GLOBE_R2023A_54009_100_V1_0.tif

# Start FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

