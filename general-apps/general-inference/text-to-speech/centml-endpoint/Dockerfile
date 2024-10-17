# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create a new user to run the application required for centml endpoints
ARG USERNAME="centml"
#Required for container to run on CentML
RUN useradd -u 1024 -m -d /home/${USERNAME} -s /bin/bash ${USERNAME} && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}
USER 1024

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run the FastAPI server using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]