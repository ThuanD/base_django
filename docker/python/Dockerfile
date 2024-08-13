FROM python:3.12.3-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.3

# Install system dependencies
RUN <<OEF
apt-get update && apt-get install -y --no-install-recommends \
    vim \
    zsh \
    curl \
    make
apt-get clean
rm -rf /var/lib/apt/lists/*
OEF

# Configure shell prompt
RUN echo "export PS1='🐳 \[\033[1;31m\]WHALE \[\033[1;36m\]\h \[\033[1;34m\]\W\[\033[0;35m\] \[\033[1;36m\]# \[\033[0m\]'" >> ~/.bashrc

# Set the working directory inside the container
WORKDIR /app

# Copy the Poetry configuration files first to leverage Docker caching
COPY ./poetry.lock ./pyproject.toml ./

# Install Poetry and project dependencies with all extras
RUN pip install poetry=="$POETRY_VERSION" && poetry install --all-extras

# Expose the port the app runs on
EXPOSE 8000

# Ensure that all static files are collected on container startup and apply migrations
CMD ["poetry", "run", "python", "manage.py", "migrate", "--settings=app.settings.docker", \
     "&&", "poetry", "run", "python", "manage.py", "createcachetable", "--settings=app.settings.docker", \
     "&&", "poetry", "run", "python", "manage.py", "collectstatic", "--noinput"]
