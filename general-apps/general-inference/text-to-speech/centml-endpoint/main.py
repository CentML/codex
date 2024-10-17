from fastapi import FastAPI, Response
from gtts import gTTS
from io import BytesIO
from pydantic import BaseModel

app = FastAPI()

# Define the request body using Pydantic model
class TextToSpeechRequest(BaseModel):
    text: str

@app.post("/text-to-speech/")
async def generate_speech(request: TextToSpeechRequest):
    # Generate the speech using gTTS
    tts = gTTS(text=request.text, lang='en', slow=False)
    
    # Create a BytesIO object to store the mp3 data
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)  # Reset the file pointer to the beginning

    # Return the mp3 audio as a streaming response
    return Response(content=mp3_fp.read(), media_type="audio/mpeg")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)