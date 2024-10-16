import os
import requests

# Use the environment variable for the API key
api_key = os.getenv("CENTML_API_KEY")  # Ensure the CENTML_API_KEY environment variable is set
if not api_key:
    raise ValueError("CENTML_API_KEY environment variable is not set.")

# CentML serverless API endpoint
endpoint = "https://api.centml.com/openai/v1/chat/completions"

# Define the payload for the request
data = {
    "model": "meta-llama/Meta-Llama-3-8B-Instruct",
    "messages": [
        {"role":"system","content":"you are helpful"},
        {"role":"user","content":"Hello"},
        {"role":"assistant","content":"Hello! It's nice to meet you. Is there something I can help you with or would you like to chat about something in particular? I'm here to lend a listening ear and offer assistance if needed."},
        {"role":"user","content":"Your Next Mesage Here"}

    ],
    "max_tokens": 2000,
    "temperature": 0.7,
    "top_p": 1,
    "n": 1,
    "stream": False,  # Streaming disabled
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stop": []
}

# Define the headers with the API key
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(endpoint, json=data, headers=headers)

# Raise an error for bad HTTP status codes
response.raise_for_status()

# Parse the response
completion = response.json()

# Print the assistant's response
print(completion["choices"][0]["message"]["content"])