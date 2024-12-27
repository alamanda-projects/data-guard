# ------- STAGE 1: Builder -------
FROM python:3.12-alpine AS builder

# Create virtual environment
RUN python -m venv /opt/venv

# Make sure to use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# Copy packages
COPY infra/python/packages/ .

# Install standard packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r stdpack.txt

# Install additional packages
RUN pip install --no-cache-dir -r addpack.txt

# ------- STAGE 2: Runtime -------
FROM python:3.12-alpine AS runtime

# Set arguments
ARG BASE_DIR=/work
ARG APP_DIR=app

# Create a non-root user
RUN adduser --system --no-create-home --shell /bin/bash --uid 1000 dgr_user

# Copy the Datadog
COPY --from=datadog/serverless-init:latest-alpine /datadog-init /dd/datadog-init

# Set current directory
WORKDIR ${BASE_DIR}/${APP_DIR}

# Copy the application
COPY app/ .

# Copy the virtualenv from the builder image
COPY --from=builder /opt/venv /opt/venv

# Make sure to use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# Install the Datadog Python tracer
RUN pip install ddtrace

# Specify the user to run the application
USER dgr_user

# Set current directory
WORKDIR ${BASE_DIR}

# Set the entrypoint to wrap application in the Datadog serverless-init process
ENTRYPOINT ["/dd/datadog-init"]

# Run the application
CMD ["ddtrace-run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8888"]