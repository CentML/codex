# Battlesnake CentML Endpoint

## Snake

- examine main.py a simple snake, and main-2.py a more advanced snake 
- make any changes you want to see

## Docker 
- Build the docker container

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t {USERNAME}/battlesnake-python:v1.0 --push .
```

## Deploying on CentML

1. Log in to CentML
Access the CentML dashboard at https://app.centml.com.

2. Navigate to General Inference
From the Home page, go to General Inference to set up the deployment.

3. Fill in Deployment Details
Provide the necessary details, including:

- Docker image name

```bash
{USERNAME}/battlesnake-python # optional replace with your image
```
- Tag (e.g., v1.0)

```bash
v1.0
```
- Port number

```bash
8000
```
- Health check path

```bash
/
```

4. Select Resource Size
Choose the resource size based on your image generation speed requirements:
- Small #Perfect for a battlesnake that doesn't use any RL models
- Medium #perfect for most ML Models for your snakes decisions
- Large # For RL model inference 

5. Click Deploy

After deployment, you will receive an `endpoint URL`.

Use that url `https://endpoint_url` in https://play.battlesnake.com to run your very own battlesnake. 

