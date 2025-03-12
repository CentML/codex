import sounddevice as sd
import numpy as np
import wave
import requests
import pyaudio
from openai import OpenAI

# API Configurations
WHISPER_ENDPOINT =  "YOUR WHISPER ENDPOINT HERE"
XTTS_ENDPOINT =  "YOUR XTTS ENDPOINT HERE"
MODEL_NAME = "YOUR CENTML MODEL HERE"
API_KEY = "YOUR CENTML API KEY HERE"

# CentML Serverless API
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.centml.com/openai/v1",
)

# Audio settings
DURATION = 5  # Recording duration in seconds
SAMPLE_RATE = 16000  # Record at 16kHz
OUTPUT_FILENAME = "recorded_audio.wav"

# 🎙️ Step 1: Record Audio
def record_audio():
    """Records audio at 16kHz in int16 format and saves it as a WAV file."""
    print("🎙️ Recording... Speak now!")
    audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype=np.int16)
    sd.wait()
    print("✅ Recording finished.")

    # Save as WAV file
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit PCM
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())

# 📝 Step 2: Send Audio to STT API
def transcribe_audio():
    """Sends the recorded audio file to the speech-to-text API and returns transcription."""
    with open(OUTPUT_FILENAME, 'rb') as audio_file:
        files = {'file': audio_file}
        response = requests.post(f"{WHISPER_ENDPOINT}/audio/transcriptions", files=files)

    if response.status_code != 200:
        print(f"❌ STT Error: {response.status_code} - {response.text}")
        raise Exception("STT API failed")

    transcribed_text = response.json().get("text", "")
    print(f"📝 Transcription: {transcribed_text}")
    return transcribed_text

# 🤖 Step 3: Send to Llama & Stream Response
def send_to_llama_streaming(text):
    """Sends transcribed text to Llama model and streams response."""
    print("🤖 Llama Response: ", end="", flush=True)  # Print in the same line

    # Enable streaming
    stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text},
        ],
        max_tokens=2000,
        temperature=0.7,
        top_p=1,
        n=1,
        stream=True,  # Enable streaming
        frequency_penalty=0,
        presence_penalty=0.5,
        stop=[]
    )

    response_text = ""
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            response_text += chunk.choices[0].delta.content

    print("\n")  # Move to new line after streaming completes
    return response_text

# 🔊 Step 4: Stream AI Voice Response
def stream_audio(text):
    """Streams AI response speech instead of saving it."""
    url = f"{XTTS_ENDPOINT}/stream"
    data = {"text": text}
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)
    
    try:
        response = requests.post(url, json=data, stream=True)
        if response.status_code != 200:
            print(f"❌ Streaming Error: {response.status_code} - {response.text}")
            return
        
        buffer = b""
        BUFFER_SIZE_THRESHOLD = 4096 * 10  # Adjust buffer size if needed
        
        for chunk in response.iter_content(chunk_size=None):
            if chunk:
                buffer += chunk
                if len(buffer) >= BUFFER_SIZE_THRESHOLD:
                    stream.write(buffer)
                    buffer = b""
        
        if buffer:
            stream.write(buffer)
    except Exception as e:
        print(f"❌ Streaming Error: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

# 🎙️🧠🔊 Step 5: Full Pipeline - Speech to AI to Speech
if __name__ == "__main__":
    record_audio()
    transcribed_text = transcribe_audio()
    
    if transcribed_text:
        ai_response = send_to_llama_streaming(transcribed_text)
        if ai_response:
            stream_audio(ai_response) 
