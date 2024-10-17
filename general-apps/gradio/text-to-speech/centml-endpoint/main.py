import torch
from transformers import pipeline
from datasets import load_dataset
from fastapi import FastAPI
from pydantic import BaseModel
from io import BytesIO
import soundfile as sf
from fastapi.responses import StreamingResponse
import uvicorn

app = FastAPI()

# Initialize the TTS pipeline with the Microsoft Speech model
tts_pipeline = pipeline("text-to-speech", model="myshell-ai/MeloTTS-English")

# Load speaker embedding dataset
embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")

# Example: Using speaker embedding index 7306 (you can adjust this dynamically based on input)
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

class TTSRequest(BaseModel):
    text: str

@app.post("/tts")
async def generate_speech(request: TTSRequest):
    # Generate the speech with the speaker embedding
    audio_output = tts_pipeline(request.text, forward_params={"speaker_embeddings": speaker_embedding})

    # Save the audio to a buffer instead of a file
    audio_data = BytesIO()
    sf.write(audio_data, audio_output["audio"], audio_output["sampling_rate"], format="WAV")
    audio_data.seek(0)

    # Return the audio buffer as a streamable response
    return StreamingResponse(audio_data, media_type="audio/wav")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    