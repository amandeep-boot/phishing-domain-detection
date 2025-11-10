# Use Python 3.11 slim image
FROM python:3.11-slim

# Install system dependencies for TensorFlow and FastAPI
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    libgomp1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set working directory
WORKDIR /workspace

# Copy requirements files
COPY requirements.txt requirements_dl.txt* ./

# Install Python dependencies (both base and DL)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    if [ -f requirements_dl.txt ]; then pip install --no-cache-dir -r requirements_dl.txt; fi

# Switch to non-root user
USER $USERNAME

# Set Python to unbuffered mode
ENV PYTHONUNBUFFERED=1
