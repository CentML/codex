# 🎙️🧠🔊 Speech-to-AI-to-Speech Pipeline

This Python script implements a seamless Speech-to-AI-to-Speech pipeline, combining voice recording, transcription, AI-generated text responses, and real-time audio streaming.

## Features
- **Audio Recording:** Captures audio input from the microphone.
- **Speech-to-Text (STT):** Converts recorded audio to text using Whisper API.
- **AI Response Generation:** Sends transcribed text to a Llama language model, streaming the response.
- **Text-to-Speech (TTS):** Streams audio of AI-generated responses using XTTS API.

## Technologies & APIs Used
- Python
- `sounddevice`, `numpy`, `wave`, `requests`, `pyaudio`
- **STT API:** Whisper (hosted on CentML)
- **Language Model:** Llama-3.2-3B-Instruct (hosted on CentML)
- **TTS API:** XTTS (hosted on CentML)

## Setup & Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
```

2. **Install dependencies:**
```bash
pip install sounddevice numpy requests pyaudio openai
```

3. **Ensure microphone and audio playback capabilities** are working correctly on your system.

4. **Launching API models on CentML:**
   - For Whisper, select `whisper_large_v3` as the image name when creating an inference deployment.
   - For XTTS, select `xtts_v2` as the image name when creating an inference deployment.

5. **Update the following variables in your script:**
```python
WHISPER_ENDPOINT =  "YOUR WHISPER ENDPOINT HERE"
XTTS_ENDPOINT =  "YOUR XTTS ENDPOINT HERE"
MODEL_NAME = "YOUR CENTML MODEL HERE"
API_KEY = "YOUR CENTML API KEY HERE"
```

## Running the Script

Simply run the Python script:
```bash
python script_name.py
```

Speak clearly into your microphone when prompted. The AI will process your voice input and respond vocally in real-time.

## Customization
- Adjust recording duration (`DURATION`) in seconds.
- Modify API endpoints and API keys within the script to match your configurations.

## Troubleshooting
- **API Errors:** Check the endpoint URLs and API keys.
- **Audio issues:** Ensure your microphone is properly configured and accessible to Python.

## License
This project is open-source and available under the MIT License.
