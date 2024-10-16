# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Gradio
RUN pip install gradio

# Make port 7860 available to the world outside this container
EXPOSE 7860

# Set environment variables (you can also pass these dynamically)
ENV CENTML_API_KEY=<your_api_key>
ENV BASE_URL=https://api.centml.com
ENV MODEL_NAME=meta-llama/Meta-Llama-3-8B-Instruct

# Run the Gradio app
CMD ["python", "app.py"]