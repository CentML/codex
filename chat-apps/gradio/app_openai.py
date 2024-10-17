import os
import gradio as gr
from openai import OpenAI

# Use environment variable for the API key
api_key = os.getenv("CENTML_API_KEY")  # Ensure the CENTML_API_KEY environment variable is set
if not api_key:
    raise ValueError("CENTML_API_KEY environment variable is not set.")

# Initialize the OpenAI client with CentML's serverless API
client = OpenAI(
    api_key=api_key,
    base_url="https://api.centml.com/openai/v1/chat/completions",
)

# Function to send a message to the CentML API and stream the response
def send_message(user_input):
    # Send the request to the CentML API with streaming enabled
    completion = client.chat.completions.create(
        model="meta-llama/Llama-3.1-405B-Instruct-FP8",
        messages=[
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": user_input}
        ],
        max_tokens=512,
        temperature=0.7,
        top_p=1,
        n=1,
        stream=True,
        frequency_penalty=0,
        presence_penalty=0,
        stop=[]
    )
    
    assistant_response = ""
    # Iterate over the streaming response and yield partial results
    for chunk in completion:
        if "content" in chunk.choices[0].delta:
            assistant_response += chunk.choices[0].delta.content
            yield assistant_response  # Stream response back to Gradio

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
    gr.Markdown("# Chat with CentML API via OpenAI Client")

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
demo.launch(share=True)