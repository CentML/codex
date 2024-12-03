from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
import torch
from outetts import InterfaceHF, HFModelConfig_v1
import io
from pydub import AudioSegment

app = FastAPI()

# Define the input data model
class TextInput(BaseModel):
    text: str
    language: str = "en"  # Default language is English

# Initialize the TTS interface
try:
    model_config = HFModelConfig_v1(
        model_path="OuteAI/OuteTTS-0.2-500M",
        language="en",  # Supported languages: en, zh, ja, ko
        dtype=torch.float16,  # Use float16 for efficiency
        additional_model_config={'attn_implementation': "default"}
    )
    tts_interface = InterfaceHF(model_version="0.2", cfg=model_config)
except Exception as e:
    raise RuntimeError(f"Failed to initialize TTS interface: {str(e)}")

@app.post("/generate", response_class=Response)
async def generate_audio(input_data: TextInput):
    """
    Generate audio from text input and return as an MP3 file.
    """
    text = input_data.text.strip()
    language = input_data.language.strip().lower()
    if not text:
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    if language not in ["en", "zh", "ja", "ko"]:
        raise HTTPException(status_code=400, detail="Unsupported language.")
    try:
        # Update the language in the model configuration
        tts_interface.cfg.language = language
        # Generate TTS output
        output = tts_interface.generate(
            text=text,
            temperature=0.7,
            repetition_penalty=1.1,
            max_length=4096
        )
        # Save the generated audio to an in-memory buffer (WAV format)
        wav_buffer = io.BytesIO()
        output.save(wav_buffer)
        wav_buffer.seek(0)
        # Convert WAV to MP3 using pydub
        audio_segment = AudioSegment.from_wav(wav_buffer)
        mp3_buffer = io.BytesIO()
        audio_segment.export(mp3_buffer, format="mp3")
        mp3_buffer.seek(0)
        # Return the MP3 audio file in the response
        return Response(content=mp3_buffer.read(), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating audio: {str(e)}")