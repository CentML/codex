import gradio as gr
import requests
from PIL import Image
from io import BytesIO
import base64
import json


# Define the API URL
API_URL = "https://{endpoint_url}/generate"


def generate_image_from_api(prompt):
    response = requests.post(API_URL, json={"prompt": prompt, "num_inference_steps": 25, "guidance_scale": 7.0})
    
    if response.status_code == 200:
        try:
            # Parse response JSON
            response_json = response.json()
            
            # Extract the base64 image string from the JSON response
            image_base64 = response.json().get("image")

            # Decode the base64 string into bytes
            image_data = base64.b64decode(image_base64)

            # Open the image using PIL and save it as a PNG file
            image = Image.open(BytesIO(image_data))
            image_path = "generated_image.png"
            image.save(image_path)

            print(f"Image saved as {image_path}")
            return image_path
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        except KeyError:
            print("Error: Could not find image in response.")
    else:
        return f"Error: {response.status_code}, {response.text}"

# Gradio interface
interface = gr.Interface(
    fn=generate_image_from_api,
    inputs="text",
    outputs="image",
    title="FLUX Image Generator"
)

if __name__ == "__main__":
    interface.launch()