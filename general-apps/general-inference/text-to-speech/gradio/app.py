import os
import requests
import gradio as gr

# Placeholder API URL for Text-to-Speech (replace with actual URL)
TTS_URL = "http://localhost:8000/text-to-speech"

# Function to send text to the TTS API
def text_to_speech(text, voice="en-US"):
    headers = {
       
        "Content-Type": "application/json"
    }
    
    data = {
        "text": text,
        "voice": voice,  # Voice configuration if supported
        "format": "mp3"  # Return as MP3 format
    }

    try:
        response = requests.post(TTS_URL, json=data, headers=headers)
        response.raise_for_status()  # Ensure the request was successful

        # Save the MP3 file and return it for playback
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        
        return "output.mp3"  # Return the path to the saved audio file

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

# Gradio interface
def gradio_tts_interface(text, voice):
    return text_to_speech(text, voice)

# UI for Gradio
with gr.Blocks() as demo:
    gr.Markdown("# Text-to-Speech App")
    
    # Text input field
    text_input = gr.Textbox(label="Enter text for TTS", placeholder="Type something...")
    
    # Dropdown for selecting a voice
    voice_select = gr.Dropdown(choices=["en-US", "en-GB", "es-ES"], label="Select Voice")
    
    # Audio output
    audio_output = gr.Audio(label="Generated Speech")

    # Button to trigger the TTS function
    convert_button = gr.Button("Convert to Speech")

    # Handle the conversion process
    convert_button.click(
        gradio_tts_interface,
        inputs=[text_input, voice_select],
        outputs=[audio_output]
    )

# Launch the Gradio app
demo.launch(server_name="0.0.0.0", server_port=7860, share=True)