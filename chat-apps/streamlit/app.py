import streamlit as st
import requests
import time
import json
import os

# Initialize session state variables for chat history and streaming status
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "streamed_response" not in st.session_state:
    st.session_state.streamed_response = ""

# Function to simulate streaming response from CentML API
def stream_response(user_message):
    # Get the CentML API key from environment variables
    api_key = os.getenv("CENTML_API_KEY")

    url = "https://api.centml.com/openai/v1/chat/completions"  # Updated to CentML API URL
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"  # Include the API key in the headers
    }

    messages = st.session_state.chat_history + [{"role": "user", "content": user_message}]

    data = {
        "model": "meta-llama/Meta-Llama-3-8B-Instruct",
        "messages": messages,
        "temperature": 0.7,
        "top_p": 1,
        "n": 1,
        "max_tokens": 100,
        "stream": True,
        "presence_penalty": 0,
        "frequency_penalty": 0,
        "ignore_eos": True
    }

    response = requests.post(url, json=data, headers=headers, verify=False, stream=True)

    # Create a placeholder for displaying streamed response
    response_placeholder = st.empty()

    # Stream response in chunks and accumulate the full response in `streamed_response`
    streamed_text = ""  # Local variable to accumulate streamed text
    for chunk in response.iter_lines():
        if chunk:
            decoded_chunk = chunk.decode('utf-8')
            if decoded_chunk == "data: [DONE]":
                break

            if "data: " in decoded_chunk:
                json_chunk = decoded_chunk.replace("data: ", "")
                json_data = json.loads(json_chunk)

                delta = json_data['choices'][0]['delta']
                chunk_text = delta.get('content', "")

                if chunk_text:
                    streamed_text += chunk_text
                    response_placeholder.markdown(f"**Assistant**: {streamed_text}")  # Update the streamed response in real-time
                    time.sleep(0.3)  # Simulate delay for smoother streaming

    st.session_state.streamed_response = streamed_text  # Store final response in session state

# Function to render chat history
def render_chat():
    for i, message in enumerate(st.session_state.chat_history):
        if message["role"] == "user":
            st.markdown(f"**You**: {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**Assistant**: {message['content']}")

# Main chat interface
st.title("Chat with CentML Serverless API")

# Input box for user message at the bottom
user_input = st.text_input("Enter your message here:")

# Send button at the bottom
if st.button("Send") and user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Clear the streamed response and start the response stream
    st.session_state.streamed_response = ""
    stream_response(user_input)

    # After the response is streamed, append it to the chat history
    st.session_state.chat_history.append({"role": "assistant", "content": st.session_state.streamed_response})
    st.text("History:")
# Render the chat history after the new message is processed
render_chat()