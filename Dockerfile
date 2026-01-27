FROM python:3.11-slim-bookworm

# Install system dependencies for LibreOffice and PDF processing
RUN apt-get update && apt-get install -y \
    libreoffice-writer \
    libreoffice-impress \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Set up your app directory
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Start command
CMD ["python", "main.py"]
