# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    EDITOR=micro \
    DJANGO_SECRET=${DJANGO_SECRET} \
    DJANGO_DEBUG=${DJANGO_DEBUG} \
    DJANGO_DOMAIN=${DJANGO_DOMAIN} \
    POSTGRES_DB=${POSTGRES_DB} \
    POSTGRES_USER=${POSTGRES_USER} \
    POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
    POSTGRES_HOST=${POSTGRES_HOST} \
    POSTGRES_PORT=${POSTGRES_PORT}

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev cron micro && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Give execution rights on the cron job
RUN chmod +x /app/entrypoint.sh /app/run_crons_server.sh /app/run_crons_mailings.sh

# Add crontab file in the cron directory
COPY crontab /etc/cron.d/crontab
RUN chmod 0644 /etc/cron.d/crontab && \
    crontab /etc/cron.d/crontab

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the application
ENTRYPOINT [ "/app/entrypoint.sh" ]