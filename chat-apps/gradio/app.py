import os
import requests
import json
import gradio as gr

# Use environment variable for the API key
api_key = os.getenv("CENTML_API_KEY")  # Ensure the CENTML_API_KEY environment variable is set
if not api_key:
    raise ValueError("CENTML_API_KEY environment variable is not set.")

# CentML serverless API endpoint
endpoint = "https://api.centml.com/openai/v1/chat/completions"

# Function to send a message to the CentML API and stream the response
def send_message(user_input):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "meta-llama/Llama-3.1-405B-Instruct-FP8",
        "messages": [
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": user_input}
        ],
        "max_tokens": 2000,
        "temperature": 0.7,
        "top_p": 1,
        "n": 1,
        "stream": True,  # Enable streaming
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": []
    }

    try:
        # Send the request and stream the response
        with requests.post(endpoint, headers=headers, json=data, stream=True) as response:
            response.raise_for_status()  # Check for HTTP errors
            assistant_response = ""
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk and chunk.startswith("data: "):
                    # Parse the streamed response
                    chunk_data = chunk[len("data: "):]
                    if chunk_data != "[DONE]":
                        content = json.loads(chunk_data)["choices"][0]["delta"].get("content", "")
                        if content:  # Only concatenate if content is not None
                            assistant_response += content
                            yield assistant_response  # Stream response back to Gradio
    except requests.exceptions.RequestException as e:
        yield f"Error connecting to server: {e}"

# Function to handle the chat interface with streaming and history
def chat_interface(user_input, chat_history):
    # Initialize chat history if None
    if chat_history is None:
        chat_history = []

    # Append the user's message to the chat history
    chat_history.append([user_input, ""])

    # Stream the assistant's response and update chat incrementally
    response_generator = send_message(user_input)
    
    assistant_response = ""
    for partial_response in response_generator:
        assistant_response = partial_response
        # Update the last assistant response in the chat history
        chat_history[-1][1] = assistant_response
        # Yield the updated chat history and an empty string for user_input
        yield chat_history, ""

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# Chat with CentML API")

    # Chat interface elements
    chat_history = gr.Chatbot(label="Chat History")
    user_input = gr.Textbox(label="Your message", placeholder="Enter your message here...")
    send_button = gr.Button("Send")

    # Send message and update the chat interface with streaming
    send_button.click(
        chat_interface,
        inputs=[user_input, chat_history],
        outputs=[chat_history, user_input],
        queue=True  # Ensure responses are queued in order
    )

# Launch the Gradio app
demo.launch(server_name="0.0.0.0", server_port=7860, share=True)