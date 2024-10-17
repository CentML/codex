import os
import requests
import json
import gradio as gr

# Use environment variable for the API key
api_key = os.getenv("CENTML_API_KEY")  # Ensure the CENTML_API_KEY environment variable is set
if not api_key:
    raise ValueError("CENTML_API_KEY environment variable is not set.")

# Define the API details for Model A and Model B
MODEL_A_CONFIG = {
    "url": "https://api.centml.com/openai/v1/chat/completions",
    "api_key": api_key,
    "model_name": "meta-llama/Llama-3.1-405B-Instruct-FP8",
    "system_prompt": "You are Model A. Debate with Model B. Always take a firm far-left stance and provide facts to support your position.",
    "history": []
}

MODEL_B_CONFIG = {
    "url": "https://api.centml.com/openai/v1/chat/completions",
    "api_key": api_key,
    "model_name": "meta-llama/Llama-3.1-405B-Instruct-FP8",
    "system_prompt": "You are Model B. Debate with Model A. Always take a firm far-right stance and provide facts to support your position.",
    "history": []
}

# Function to send a message to the CentML API and stream the response
def send_message(config, user_input):
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }
    
    # Prepare the conversation messages including the system prompt and user message
    config['history'].append({"role": "user", "content": user_input})
    messages = [{"role": "system", "content": config['system_prompt']}] + config['history']

    data = {
        "model": config["model_name"],
        "messages": messages,
        "max_tokens": 200,
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
        with requests.post(config["url"], headers=headers, json=data, stream=True) as response:
            response.raise_for_status()  # Check for HTTP errors
            assistant_response = ""
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk and chunk.startswith("data: "):
                    chunk_data = chunk[len("data: "):]
                    if chunk_data != "[DONE]":
                        content = json.loads(chunk_data)["choices"][0]["delta"].get("content", "")
                        if content:  # Only concatenate if content is not None
                            assistant_response += content
                            yield assistant_response  # Stream response back to Gradio
    except requests.exceptions.RequestException as e:
        yield f"Error connecting to server: {e}"

# Function to handle the debate between Model A and Model B
def debate(user_input, chat_history, num_rounds):
    # Initialize chat history if None
    if chat_history is None:
        chat_history = []

    # Append the user's message as the topic
    chat_history.append([f"You: {user_input}", None])

    model_a_response = ""
    model_b_response = ""  # Reset Model B's response here

    # Debate for the specified number of rounds
    for round_num in range(int(num_rounds)):
        # Streaming response from Model A
        for partial_response in send_message(MODEL_A_CONFIG, user_input):
            model_a_response = partial_response
            # Update the last message with Model A's streaming response
            chat_history[-1][1] = f"Model A:\n Topic: {user_input}\n {model_a_response}"
            yield chat_history, ""

        # Append the full response from Model A into history
        MODEL_A_CONFIG['history'].append({"role": "assistant", "content": model_a_response})

        # Reset Model B's response
        model_b_response = ""

        # Streaming response from Model B (responding to Model A)
        for partial_response in send_message(MODEL_B_CONFIG, model_a_response):
            model_b_response = partial_response
            # Update the last message with Model B's streaming response (no extra bubbles)
            if len(chat_history) > 1 and chat_history[-1][0].startswith("Model B"):
                chat_history[-1][0] = f"Model B \n Topic: {user_input}\n {model_b_response}"
            else:
                chat_history.append([f"Model B: {model_b_response}", None])
            yield chat_history, ""

        # Append the full response from Model B into history
        MODEL_B_CONFIG['history'].append({"role": "assistant", "content": model_b_response})

        # Model B's response becomes the new input for Model A
        user_input = model_b_response

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# LLM Debate: Model A vs Model B")

    chat_history = gr.Chatbot(label="Debate History")
    user_input = gr.Textbox(label="Your message", placeholder="Enter the debate topic here...")
    rounds_slider = gr.Slider(minimum=1, maximum=3, step=1, value=1, label="Number of Debate Rounds")
    send_button = gr.Button("Send")

    # Send message and update the chat interface with streaming
    send_button.click(
        debate,
        inputs=[user_input, chat_history, rounds_slider],
        outputs=[chat_history, user_input],
        queue=True  # Ensure responses are queued in order
    )

# Launch the Gradio app
demo.launch(server_name="0.0.0.0", server_port=7860, share=True)