# Text To Speech Service on CentML 

## Docker 

- Linux
```bash
docker build -t tts-fastapi .

docker run -d -p 8000:8000 tts-fastapi
```

- MacOS
```bash
docker buildx build --platform linux/amd64,linux/arm64 -t {docker_uname}/tts-fastapi --push .
```

## Usage Testing

```bash
curl -X POST "http://{endpoint_url}/text-to-speech/" -H "Content-Type: application/json" -H "Content-Type: application/json"  -d '{"text": "Hello, welcome to the FastAPI text-to-speech service!"}' --output speech.mp3'
```

- Use the included gradio app for a nice UI experience. 