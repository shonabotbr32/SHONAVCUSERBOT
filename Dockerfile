FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    pulseaudio \
    alsa-utils \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for session files
RUN mkdir -p /app/sessions

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PULSE_SERVER=unix:/tmp/pulseaudio.socket

# Run the bot
CMD ["python", "main.py"]
