# Use a lightweight base image
FROM python:3.11.8-alpine3.18

# Create the application directory
RUN mkdir -p /pytudo_docker
WORKDIR /pytudo_docker

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the entire local project into the container
COPY . .

# Create and activate virtual environment
RUN python -m venv /venv
ENV PATH="/scripts:/venv/bin:$PATH"

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    adduser --disabled-password --no-create-home duser && \
    mkdir -p /staticfiles && \
    mkdir -p /media && \
    chown -R duser:duser /venv && \
    chown -R duser:duser /staticfiles && \
    chown -R duser:duser /media && \
    chmod -R 755 /staticfiles && \
    chmod -R 755 /media && \
    chmod -R +x /scripts


USER duser

EXPOSE 8000

# Start the server
CMD ["comandos.sh"]