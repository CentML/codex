#!/bin/bash
# ASCII Art Banner
function print_banner() {
    echo """ 
                                                                                                                                             
                                                                                                                                         
        CCCCCCCCCCCCC                                               tttt          MMMMMMMM               MMMMMMMMLLLLLLLLLLL             
     CCC::::::::::::C                                            ttt:::t          M:::::::M             M:::::::ML:::::::::L             
   CC:::::::::::::::C                                            t:::::t          M::::::::M           M::::::::ML:::::::::L             
  C:::::CCCCCCCC::::C                                            t:::::t          M:::::::::M         M:::::::::MLL:::::::LL             
 C:::::C       CCCCCC    eeeeeeeeeeee    nnnn  nnnnnnnn    ttttttt:::::ttttttt    M::::::::::M       M::::::::::M  L:::::L               
C:::::C                ee::::::::::::ee  n:::nn::::::::nn  t:::::::::::::::::t    M:::::::::::M     M:::::::::::M  L:::::L               
C:::::C               e::::::eeeee:::::een::::::::::::::nn t:::::::::::::::::t    M:::::::M::::M   M::::M:::::::M  L:::::L               
C:::::C              e::::::e     e:::::enn:::::::::::::::ntttttt:::::::tttttt    M::::::M M::::M M::::M M::::::M  L:::::L               
C:::::C              e:::::::eeeee::::::e  n:::::nnnn:::::n      t:::::t          M::::::M  M::::M::::M  M::::::M  L:::::L               
C:::::C              e:::::::::::::::::e   n::::n    n::::n      t:::::t          M::::::M   M:::::::M   M::::::M  L:::::L               
C:::::C              e::::::eeeeeeeeeee    n::::n    n::::n      t:::::t          M::::::M    M:::::M    M::::::M  L:::::L               
 C:::::C       CCCCCCe:::::::e             n::::n    n::::n      t:::::t    ttttttM::::::M     MMMMM     M::::::M  L:::::L         LLLLLL
  C:::::CCCCCCCC::::Ce::::::::e            n::::n    n::::n      t::::::tttt:::::tM::::::M               M::::::MLL:::::::LLLLLLLLL:::::L
   CC:::::::::::::::C e::::::::eeeeeeee    n::::n    n::::n      tt::::::::::::::tM::::::M               M::::::ML::::::::::::::::::::::L
     CCC::::::::::::C  ee:::::::::::::e    n::::n    n::::n        tt:::::::::::ttM::::::M               M::::::ML::::::::::::::::::::::L
        CCCCCCCCCCCCC    eeeeeeeeeeeeee    nnnnnn    nnnnnn          ttttttttttt  MMMMMMMM               MMMMMMMMLLLLLLLLLLLLLLLLLLLLLLLL
                                                                                                                                         

    """
    echo "                                              Chat with LLaMA - Powered by CentML API    "
    echo "============================================================================================================================================"
}

# Function to interact with the LLaMA API and stream responses
function llama_chat() {
    # Print ASCII art banner
    print_banner

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
          --arg model "meta-llama/Llama-3.1-405B-Instruct-FP8" \
          '{
            model: $model,
            messages: $messages,
            temperature: 0.7,
            top_p: 1,
            n: 1,
            max_tokens: 2000,
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