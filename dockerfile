# Use the official Python image from the Docker Hub
FROM python:3.12.3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install Poetry
RUN pip install --upgrade pip \
    && pip install poetry

# Create and set the working directory
WORKDIR /app

# Copy pyproject.toml and poetry.lock to the working directory
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry add psycopg2-binary \
    && poetry install --no-root

# Copy the rest of the application code to the working directory
COPY . /app/

# Collect static files (optional)
RUN python manage.py collectstatic --noinput --settings=config.settings

# Expose port 8000
EXPOSE 8000

# Run the application
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
