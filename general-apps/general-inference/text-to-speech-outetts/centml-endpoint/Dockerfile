# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && \
    apt-get install -y git ffmpeg gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir torch==2.0.1 transformers==4.35.0

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY main.py .

# Create a new user to run the application required for centml endpoints
ARG USERNAME="centml"
#Required for container to run on CentML
RUN useradd -u 1024 -m -d /home/${USERNAME} -s /bin/bash ${USERNAME} && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}
USER 1024

# Make port 8000 available to the world outside this container
EXPOSE 8000
# Command to run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
