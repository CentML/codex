## sd_endpoint.py
import torch
from fastapi import FastAPI
from pydantic import BaseModel
from diffusers import StableDiffusion3Pipeline
from typing import Optional
from PIL import Image
import io
import base64
import uvicorn

# Load the Stable Diffusion 3 model from stability.ai
pipe = StableDiffusion3Pipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-large-turbo",
    torch_dtype=torch.float16,
    safety_checker=None
).to("cuda")

# Define the FastAPI app
app = FastAPI()

# Define the request body model
class ImagePrompt(BaseModel):
    prompt: str
    num_inference_steps: Optional[int] = 35
    guidance_scale: Optional[float] = 7.0

# Function to convert image to base64
def image_to_base64(image: Image.Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

# Define the '/generate' endpoint
@app.post("/generate")
async def generate_image(image_prompt: ImagePrompt):
    # Generate the image using the provided prompt
    image = pipe(
        image_prompt.prompt,
        num_inference_steps=image_prompt.num_inference_steps,
        guidance_scale=image_prompt.guidance_scale
    ).images[0]

    # Convert image to base64
    image_base64 = image_to_base64(image)

    # Return the base64 image
    return {"image": image_base64}

# Run the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)