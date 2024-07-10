

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/


# Install Rust compiler

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11
# Prevents Python from writing pyc files.


# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.


WORKDIR /app
COPY . .

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN pip install --no-cache-dir --upgrade -r requirements.txt



# Copy the source code into the container.

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD uvicorn main:app --reload --host 0.0.0.0 --port 8000

