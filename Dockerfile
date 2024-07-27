# Use the official Python image from the Docker Hub.
FROM python:3.10.12

# Install system dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add a new user
RUN adduser --disabled-password --gecos '' django_user

# Create necessary directories and set permissions
RUN mkdir -p /var/app/socket /var/app/logs \
    && chown -R django_user:django_user /var/app

# Switch to the new user
USER django_user

# Set environment variables
ENV PATH="/home/django_user/.local/bin:$PATH"
ENV PYTHONUNBUFFERED=1
# Comment below line for running on local
ENV ENVIRONMENT=production

# Set the working directory
WORKDIR /var/app

# Copy the requirements.txt
COPY requirements.txt /var/app/

# Install Python dependencies
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python -c "import nltk; nltk.download('punkt')"

# Copy project files
COPY --chown=django_user:django_user . /var/app/

# Expose the port the app runs on
EXPOSE 8000

# Run the Django production server
CMD bash ./gunicorn_start django_user
