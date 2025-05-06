FROM python:3.9-slim

WORKDIR /app

# Install PostgreSQL client for wait-for-db script
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make wait script executable
RUN chmod +x /app/wait-for-db.sh

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Wait for database to be ready before starting the app
CMD ["/app/wait-for-db.sh", "postgres", "5432", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]