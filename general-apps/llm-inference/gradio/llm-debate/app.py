import os
import time
import requests
import json
import gradio as gr

# Use environment variable for the API key
model_a_api_key = os.getenv("MODEL_A_API_KEY")
model_b_api_key = os.getenv("MODEL_B_API_KEY")
# Ensure the CENTML_API_KEY environment variable is set
if not model_a_api_key:
    raise ValueError("MODEL_A_API_KEY environment variable is not set.")
if not model_b_api_key:
    raise ValueError("MODEL_B_API_KEY environment variable is not set.")

model_a_url = os.getenv(
    "MODEL_A_URL", "https://api.centml.com/openai/v1/chat/completions"
)
model_b_url = os.getenv(
    "MODEL_B_URL", "https://api.centml.com/openai/v1/chat/completions"
)

model_a_model_name = os.getenv("MODEL_A", "deepseek-ai/DeepSeek-V3-0324")
model_b_model_name = os.getenv("MODEL_B", "deepseek-ai/DeepSeek-V3-0324")

model_a_human_name = os.getenv("HUMAN_A", "Mark Carney")
model_b_human_name = os.getenv("HUMAN_B", "Pierre Poilievre")


# Define the API details for Model A and Model B
MODEL_A_CONFIG = {
    "url": model_a_url,
    "api_key": model_a_api_key,
    "model_name": model_a_model_name,
    "system_prompt": f"You are {model_a_human_name}. Debate with {model_b_human_name}. "
    "Always take a firm left stance, use your personal experience, and provide facts to"
    " support your position.",
    "history": [],
}

MODEL_B_CONFIG = {
    "url": model_b_url,
    "api_key": model_b_api_key,
    "model_name": model_b_model_name,
    "system_prompt": f"You are {model_b_human_name}. Debate with {model_a_human_name}. "
    "Always take a firm right stance, use your personal experience, and provide facts "
    "to support your position.",
    "history": [],
}


# Function to send a message to the CentML API and stream the response
def send_message(config, user_input):
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
    }

    # Prepare the conversation messages including the system prompt and user message
    config["history"].append({"role": "user", "content": user_input})
    messages = [{"role": "system", "content": config["system_prompt"]}] + config[
        "history"
    ]

    data = {
        "model": config["model_name"],
        "messages": messages,
        "max_tokens": 8192,
        "temperature": 0.7,
        "top_p": 1,
        "n": 1,
        "stream": True,  # Enable streaming
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "stop": [],
    }

    try:
        # Send the request and stream the response
        ttft = None  # Time (in s) to first token.
        tps = None  # Tokens per second.
        tic = time.perf_counter()
        with requests.post(
            config["url"], headers=headers, json=data, stream=True
        ) as response:
            response.raise_for_status()  # Check for HTTP errors
            assistant_response = ""
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk and chunk.startswith("data: "):
                    if not assistant_response:
                        ttft = time.perf_counter() - tic
                    else:
                        tps = 1.0 / (time.perf_counter() - tic)
                    chunk_data = chunk[len("data: ") :]
                    if chunk_data != "[DONE]":
                        delta = json.loads(chunk_data)["choices"][0]["delta"]
                        content = delta.get("content", "")
                        if not content:
                            content = delta.get("reasoning_content", "")
                        if content:  # Only concatenate if content is not None
                            assistant_response += content
                            yield assistant_response, ttft, tps  # Stream response back to Gradio
                            tic = time.perf_counter()
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

    model_a_signature = f"{model_a_human_name} ({model_a_model_name} @ {model_a_url})"
    model_b_signature = f"{model_b_human_name} ({model_b_model_name} @ {model_b_url})"

    # Debate for the specified number of rounds
    for round_num in range(int(num_rounds)):
        # Streaming response from Model A
        for partial_response, ttft, tps in send_message(MODEL_A_CONFIG, user_input):
            model_a_response = partial_response
            # Update the last message with Model A's streaming response
            chat_history[-1][1] = f"{model_a_signature}:\n{model_a_response}"
            yield chat_history, "", f"{model_a_signature} : {ttft}", f"{model_a_signature} : {tps}"

        # Append the full response from Model A into history
        MODEL_A_CONFIG["history"].append(
            {"role": "assistant", "content": model_a_response}
        )

        # Reset Model B's response
        model_b_response = ""

        # Streaming response from Model B (responding to Model A)
        chat_history.append([None, None])
        for partial_response, ttft, tps in send_message(
            MODEL_B_CONFIG, model_a_response
        ):
            model_b_response = partial_response
            chat_history[-1][0] = f"{model_b_signature}\n{model_b_response}"
            yield chat_history, "", f"{model_b_signature} : {ttft}", f"{model_b_signature} : {tps}"

        # Append the full response from Model B into history
        MODEL_B_CONFIG["history"].append(
            {"role": "assistant", "content": model_b_response}
        )

        # Model B's response becomes the new input for Model A
        user_input = model_b_response


# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown(f"# LLM Debate: {model_a_human_name} vs {model_b_human_name}")

    chat_history = gr.Chatbot(label="Debate History")
    user_input = gr.Textbox(
        label="Your message", placeholder="Enter the debate topic here..."
    )
    rounds_slider = gr.Slider(
        minimum=1, maximum=10, step=1, value=1, label="Number of Debate Rounds"
    )
    send_button = gr.Button("Send")
    ttft = gr.Textbox(label="Time (in seconds) to first token")
    tps = gr.Textbox(label="Tokens per second")

    # Send message and update the chat interface with streaming
    send_button.click(
        debate,
        inputs=[user_input, chat_history, rounds_slider],
        outputs=[chat_history, user_input, ttft, tps],
        queue=True,  # Ensure responses are queued in order
    )

# Launch the Gradio app
demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
