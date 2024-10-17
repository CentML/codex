import base64
import requests
from PIL import Image
from io import BytesIO

def generate_image(prompt):
    # Fixed parameters

    url = "https://{endpoint_url}/generate" # REPLACE WITH YOUR URL 
    num_inference_steps = 37
    guidance_scale = 7.0

    data = {
        "prompt": prompt,
        "num_inference_steps": num_inference_steps,
        "guidance_scale": guidance_scale
    }

    try:
        # Send the POST request and get the response
        response = requests.post(url, json=data)
        response.raise_for_status()

        # Extract the base64 image string from the JSON response
        image_base64 = response.json().get("image")

        # Decode the base64 string into bytes
        image_data = base64.b64decode(image_base64)

        # Open the image using PIL and save it as a PNG file
        image = Image.open(BytesIO(image_data))
        image_path = "generated_image.png"
        image.save(image_path)

        print(f"Image saved as {image_path}")
        
        # Open the saved image
        image.show()

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except KeyError:
        print("Error: Could not find image in response.")

if __name__ == "__main__":
    while True:
        # Get user input for prompt
        prompt = input("Enter the prompt (or 'exit' to quit): ")
        if prompt.lower() == 'exit':
            break

        # Call the function to generate and display the image
        generate_image(prompt)
