# Use slim Python image to minimize size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app.py .

# Expose application port
EXPOSE 5000

# Run as non-root user for security
RUN useradd -r -s /bin/false appuser
USER appuser

# Start Flask application
CMD ["python", "app.py"]
