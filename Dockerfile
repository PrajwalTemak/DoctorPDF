# Use the official Python slim image
FROM python:3.11-slim-bookworm

# Install ALL system dependencies in one single RUN command
# We use pdftk-java because pdftk is often unavailable in slim Bookworm repos
RUN apt-get update && apt-get install -y \
    libreoffice-writer \
    libreoffice-impress \
    libmagic1 \
    poppler-utils \
    pdftk-java \
    && rm -rf /var/lib/apt/lists/*

# Set up your app directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8080

# Command to run the application
CMD ["python", "main.py"]