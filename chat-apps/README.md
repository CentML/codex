# Chat Apps

This directory contains various implementations of AI-based chat applications using different frameworks and libraries. Each subdirectory demonstrates how to interact with the CentML API or OpenAI API using different programming languages and technologies.

## Directory Overview

1. bash

	•	Contains an example of using curl commands in a bash script to interact with the CentML API.
	•	Suitable for lightweight terminal-based chat applications or command-line scripting.
	•	Simple and easy to integrate with other bash utilities.

### Technologies: Bash, curl

2. gradio

	•	A Gradio interface that creates a simple web app for chatting with the AI.
	•	Gradio provides an easy-to-use UI for AI applications without requiring any frontend development experience.
	•	Quickly launch interactive demos directly in the browser.

### Technologies: Python, Gradio

3. html

	•	A pure HTML and JavaScript chat interface that interacts with the API using fetch requests.
	•	Can be easily integrated into any web project or embedded in a web page for simple interactions.
	•	Includes basic UI for sending and receiving messages in a browser environment.

### Technologies: HTML, JavaScript, CSS

4. openai

	•	Contains an example of using the official OpenAI Python library to communicate with the API.
	•	The implementation includes managing API calls for completions and streaming chat responses.
	•	Works well for those already using OpenAI’s libraries and models.

### Technologies: Python, OpenAI API

5. requests

	•	Demonstrates how to use the requests library in Python to interact with the CentML or OpenAI API.
	•	Provides a simple yet powerful way to make HTTP requests, handle responses, and build a command-line or script-based chat interface.
	•	Suitable for those who want minimal dependencies.

### Technologies: Python, requests library

6. streamlit

	•	Streamlit-based web application for interacting with the CentML API.
	•	Provides a rich UI for chat applications with minimal code and fast deployment.
	•	Allows for easy real-time interaction, text input, and response streaming.

### Technologies: Python, Streamlit

7. swift

	•	Contains a SwiftUI-based chat application that interacts with the CentML API using native Swift.
	•	Provides a mobile-friendly or macOS-compatible chat experience with real-time streaming of responses.
	•	Ideal for iOS/macOS developers looking to build native AI chat applications.

### Technologies: Swift, SwiftUI

## Usage

Each subdirectory contains specific setup and usage instructions in its own README.md or in the provided source files. Refer to the specific subdirectory for detailed instructions on how to install dependencies, set up the environment, and run the application.

## API Key and Configuration

Most examples in this directory will require an API key from CentML. Make sure to replace any placeholders with your actual API key in the respective files before running the applications. Most of the apps automatically use the CENTML_API_KEY env variable if set. 

```bash 
export CENTML_API_KEY="your_actual_api_key"
```

For web-based apps, be sure to also configure the appropriate URL endpoints and API keys as needed.

Feel free to explore each implementation to understand how the chat application can be built using different languages and frameworks.

