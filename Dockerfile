# Use Python 3.13 as base (note: as of now, Python 3.13 is still in preview)
FROM python:3.13

# Create /app and /app/storage directories
RUN mkdir /app /app/storage
WORKDIR /app

# Environment variables for Python
ENV PYTHONPATH="${PYTHONPATH}:/app"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy in requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project source code into the container
COPY . /app/

# Project-specific config for an example superuser & default DB path
ENV DJANGO_SUPERUSER_USERNAME="admin"
ENV DJANGO_SUPERUSER_PASSWORD="admin"
ENV DJANGO_SUPERUSER_EMAIL="admin@localhost"
ENV DATABASE_URL="sqlite:////app/storage/db.sqlite3"

# Expose port 8000 for our Django app
EXPOSE 8000

# When the container starts, run the entrypoint script
CMD ["sh", "/app/docker_entrypoint.sh"]
