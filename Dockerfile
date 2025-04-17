# Stage 1: Build frontend assets
FROM node:18-slim AS frontend-builder
WORKDIR /app

# Copy package files
COPY package.json tailwind.config.js ./

# Create directory structure
RUN mkdir -p static/css

# Copy CSS files
COPY static/css/input.css ./static/css/

# Install dependencies and build
RUN npm install
RUN npm run build

# Stage 2: Python application
FROM python:3.8-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxinerama1 \
    libxi6 \
    libfreetype6 \
    libfontconfig1 \
    libpng-dev \
    libjpeg-dev \
    libtiff-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p static/css drawings output

# Copy the application code
COPY . .

# Copy built CSS from frontend stage
COPY --from=frontend-builder /app/static/css/main.css ./static/css/

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run the application with auto-reload
CMD ["flask", "run", "--host=0.0.0.0", "--debugger"] 