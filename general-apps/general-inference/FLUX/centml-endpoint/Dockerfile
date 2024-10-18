# Use the NVIDIA devel image to ensure CUDA development tools are available
FROM pytorch/pytorch:2.4.1-cuda11.8-cudnn9-devel

# Set a default working directory
WORKDIR /app


# Set CUDA_HOME to point to the CUDA installation
ENV CUDA_HOME=/usr/local/cuda

# Install Rust using rustup (set to stable toolchain)
#RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
#ENV PATH="/root/.cargo/bin:${PATH}"
#RUN rustup default stable

# Install flash-attn
#RUN pip install --upgrade flash-attn
#RUN pip install --upgrade torch torchvision
#RUN pip install --upgrade apex

# Copy the requirements file into the container
COPY requirements.txt /app/requirements.txt

# Install the Python dependencies
RUN pip install -r requirements.txt

# Create a new user to run the application required for centml endpoints
ARG USERNAME="centml"

RUN useradd -u 1024 -m -d /home/${USERNAME} -s /bin/bash ${USERNAME} && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}
USER 1024

# Copy the rest of the application into the container
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Set the entrypoint to run the FastAPI app via Uvicorn
#ENTRYPOINT ["python", "main.py"]