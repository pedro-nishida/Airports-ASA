FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create wait-for-db script if it doesn't exist
RUN if [ ! -f /app/wait-for-db.sh ]; then \
    echo '#!/bin/bash\n\
echo "Waiting for PostgreSQL..."\n\
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do\n\
  sleep 1\n\
done\n\
echo "PostgreSQL is ready"\n\
exec "$@"' > /app/wait-for-db.sh; \
fi

# Make wait script executable
RUN chmod +x /app/wait-for-db.sh

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Default command - can be overridden in Kubernetes
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]