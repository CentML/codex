#!/bin/bash

# Function to interact with the LLaMA API and stream responses
function llama_chat() {
    # Initialize an array to store the conversation history
    messages=(
        '{"role": "system", "content": "You are a helpful assistant."}'
    )

    while true; do
        # Prompt the user for input
        read -p "You: " user_input
        
        # Check if the user wants to exit
        if [[ "$user_input" == "exit" ]]; then
            echo "Goodbye!"
            break
        fi

        # Add the user's message to the conversation history
        messages+=('{"role": "user", "content": "'"$user_input"'"}')

        # Prepare the JSON payload with jq to ensure proper JSON formatting
        json_payload=$(jq -n \
          --argjson messages "$(printf '%s\n' "${messages[@]}" | jq -s .)" \
          --arg model "meta-llama/Meta-Llama-3-8B-Instruct" \
          '{
            model: $model,
            messages: $messages,
            temperature: 0.7,
            top_p: 1,
            n: 1,
            max_tokens: 1000,
            stream: true,
            presence_penalty: 0,
            frequency_penalty: 0,
            ignore_eos: true
          }')

        # Send the request to the LLaMA API and stream the response
        response=""
        curl -s -X POST https://api.centml.com/openai/v1/chat/completions \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${CENTML_API_KEY}" \
        -d "$json_payload" | while IFS= read -r line; do
            clean_line=$(echo "$line" | sed 's/^data: //' | jq -r '.choices[].delta.content' 2>/dev/null)
            if [[ -n "$clean_line" && "$clean_line" != "null" ]]; then
                # Clean the line to remove unnecessary spaces before punctuation
                clean_line=$(echo "$clean_line" | sed -E 's/ +([.,!?])/\1/g' | tr -s ' ')
                echo -n "$clean_line"
                response+="$clean_line"
            fi
        done
        echo -e "\n"

        # Add the assistant's response to the conversation history
        messages+=('{"role": "assistant", "content": "'"$response"'"}')
    done
}

# Run the chat function
llama_chat