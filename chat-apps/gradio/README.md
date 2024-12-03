# CentML Chat App with Gradio

This Gradio-based web app allows you to interact with the CentML Serverless API . It streams the assistant's responses in real-time, providing a conversational interface where users can chat with an AI assistant.

## Features

- **Real-time Chat**: The assistant responds in real-time to your inputs by streaming responses as they are generated.
- **Easy-to-Use Interface**: The Gradio interface allows for a clean and intuitive user experience.

## Prerequisites

Before running the app, ensure that you have the following:

1. **Python 3.10+** installed on your machine.
2. **Gradio** and other necessary Python libraries. You can install these via `pip` (see instructions below).
3. A valid **CentML API key**. The API key should be stored in an environment variable called `CENTML_API_KEY`.

## Usage
### Docker File

1. Docker
```bash
export CENTML_API_KEY="your-api-key-here"
docker build -t gradio-app .   
docker run -p 7860:7860 -e CENTML_API_KEY=${CENTML_API_KEY} gradio-app
```

2. Open Browser
- navigate to 
http://localhost:7860

### Local
1. Enter chat-apps/gradio directory

```bash
   cd chat-apps/gradio
```

2.	Set up a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate 
```

3.	Install the required dependencies:
```bash
pip install -r requirements.txt
```
Note: If you don’t have/can't find a requirements.txt file, you can install the necessary libraries like this:
```bash
pip install gradio requests
```

4.	Set the CentML API key as an environment variable:
```bash
export CENTML_API_KEY="your-api-key-here"
```
Replace "your-api-key-here" with your actual CentML API key.

## Running the App

To run the Gradio app, execute the following command:
```bash
python app.py
```
This will launch a local Gradio interface in your browser. If the app doesn’t open automatically, you can access it by navigating to the URL shown in your terminal (usually http://127.0.0.1:7860/). You will also get a free 72 hour public URL to share and use from anywhere. 



## Customization

- Model: If you want to change the model or parameters such as temperature or max_tokens, you can modify the data dictionary in the send_message function in app.py.
- UI Layout: You can adjust the layout of the interface by modifying the Gradio components in the gr.Blocks section.

## Troubleshooting

- Error Connecting to API: If you encounter an error connecting to the CentML API, ensure that your API key is valid and set in the environment variable CENTML_API_KEY.
- Python Version: Ensure you are using Python 3.8 or higher.
- Dependencies: Make sure you have installed all the necessary dependencies (Gradio and Requests).

