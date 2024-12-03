# Text To Speech Service on CentML 

## Docker 

- Linux
```bash
docker build -t outetts-fastapi .

docker run -d -p 8000:8000 outetts-fastapi
```

- MacOS
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t {docker_uname}/outetts-fastapi --push .
```

## Usage Testing

```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello, welcome to the FastAPI text-to-speech service!", "language": "en"}' \
     --output speech.mp3
```

- Use the included gradio app for a nice UI experience. 