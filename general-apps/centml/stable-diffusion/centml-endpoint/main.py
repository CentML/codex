from fastapi import FastAPI
from pydantic import BaseModel
from diffusers import FluxPipeline
from typing import Optional
from PIL import Image
import io
import base64
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import torch

# Load the Flux model from black-forest-labs with mixed precision for GPU optimization
pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-dev",
    torch_dtype=torch.float16  # Use float16 for mixed precision (reduces memory usage and speeds up inference)
).to("cuda" if torch.cuda.is_available() else "cpu")

# Optionally, enable model CPU offload to save VRAM (uncomment if needed)
# pipe.enable_model_cpu_offload()

# Define the FastAPI app
app = FastAPI()

# Add CORS middleware to allow requests from web front-ends (like HTML or JS apps)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, you can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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