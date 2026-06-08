FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Workdir
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Expose Flask port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "wsgi:app"]