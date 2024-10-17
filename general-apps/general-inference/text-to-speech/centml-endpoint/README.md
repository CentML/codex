# UNDER CONSTRUCTION

## Docker 
```bash
docker build -t tts-fastapi .

docker run -d -p 8000:8000 tts-fastapi
```

## Usage Testing

```bash
curl -X POST "http://localhost:8000/tts" -H "Content-Type: application/json" -d '{"text": "Hello, this is a test of the Bark text to speech system."}'
```