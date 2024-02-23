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
COPY scripts /scripts

# Create and activate virtual environment
RUN python -m venv /venv
ENV PATH="/scripts:/venv/bin:$PATH"

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    mkdir -p /staticfiles && \
    mkdir -p /media && \
    chmod -R 775 /staticfiles && \
    chmod -R 775 /media && \
    chmod -R +x /scripts

EXPOSE 8000

# Start the server
CMD ["comandos.sh"]