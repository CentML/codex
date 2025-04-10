# CentML Serverless Chat

This Bash script interacts with the LLaMA model via CentML’s serverless API to create a simple real-time chat interface. The assistant provides helpful responses to user inputs, allowing you to have a back-and-forth conversation.

## Features

- Continuously streams responses from the CentML API.

- Keeps track of the conversation history between the user and the assistant.

- Supports dynamic interaction and real-time updates with each message.

## Prerequisites

Before running the script, ensure that you have:

1.	A valid CentML API key.
2.	jq installed on your system (for JSON manipulation). You can install it using:

```bash
sudo apt-get install jq    # On Ubuntu/Debian
brew install jq            # On macOS
```


## Getting Started

1. Directory

enter the chat-apps/bash directory

2. Make the Script Executable

Make the script executable by running the following command:

```bash
chmod +x chat.sh
```

3. Set Your CentML API Key

Export your CentML API key as an environment variable:

```bash
export CENTML_API_KEY="your-api-key"
```

Replace "your-api-key" with your actual CentML API key.

4. Run the Chat Script

Now you’re ready to run the chat script. Start the chat session by executing:

```bash
./chat.sh
```

5. Exit the Chat

To exit the chat, simply type exit at any prompt, and the session will end.

### Example Chat Session

```bash
$ ./chat.sh
You: hi
Hi! It's nice to meet you! Is there something I can help you with or would you like to chat?

You: Tell me about quantum mechanics. 
Quantum mechanics! It's a fascinating and complex branch of physics that has revolutionized our understanding of the tiny world at the atomic and subatomic level. In fact, it's one of the most successful theories in the history of science.So, what is quantum mechanics? In simple terms, it's a set of mathematical equations that describe the behavior of matter and energy at the smallest scales. It's called "quantum" because it deals with the smallest units of matter and energy, which are

You: exit
Goodbye!
```

## Troubleshooting

- API Errors: If the script fails to fetch responses, check your API key and ensure it is valid.
- Response Formatting: The script includes basic string formatting to clean up the assistant’s responses, removing unnecessary spaces before punctuation.
- Missing jq: Make sure you have jq installed. If not, the script will fail when handling JSON responses.

