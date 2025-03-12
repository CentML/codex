from openai import OpenAI
import os
import json
import time
from weather_utils import get_weather

# Supply your API key from https://app.centml.com/user/vault
api_key = os.environ.get("CENTML_API_KEY")
assert api_key is not None, "Please provide an API Key"
base_url = "https://api.centml.com/openai/v1"

# Define a tool (function) the model can call
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for a given location.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City and country e.g. Bogotá, Colombia"
                }
            },
            "required": ["location"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

def process_tool_calling(client, model_id, messages, available_functions=None):
    """
    Process a tool calling request with proper error handling.
    
    Args:
        client: The OpenAI client
        model_id: The ID of the model to use
        messages: The messages to send to the model
        available_functions: Dictionary mapping function names to their implementations
        
    Returns:
        str: response_text: The text response from the model
    """
    if available_functions is None:
        available_functions = {"get_weather": get_weather}
        
    response_text = ""
    
    try:
        # Create a chat completion request with the defined prompt and schema
        chat_completion = client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=4096,
            tools=tools,
            tool_choice="auto"  # Let the model decide when to use tools
        )
        
        tool_calls = chat_completion.choices[0].message.tool_calls
        if tool_calls:
            # Create a properly formatted assistant message
            assistant_message = {
                "role": "assistant",
                "content": chat_completion.choices[0].message.content or "",  # Ensure content is a string
                "tool_calls": [
                    {
                        "id": tool_call.id,
                        "type": tool_call.type,
                        "function": {
                            "name": tool_call.function.name,
                            "arguments": tool_call.function.arguments
                        }
                    } for tool_call in tool_calls
                ]
            }
            
            # Start with the original prompt and add the assistant's response
            updated_messages = messages + [assistant_message]
            
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"Function name: {function_name}, Function args: {function_args}")
                
                function_response = function_to_call(location=function_args.get("location"))
                print(f"Function response: {function_response}")
                
                # Add the tool response
                updated_messages.append({ 
                    "tool_call_id": tool_call.id, 
                    "role": "tool", 
                    "name": function_name, 
                    "content": function_response
                })
            
            # Make the second API call with properly formatted messages
            second_response = client.chat.completions.create( 
                model=model_id, 
                messages=updated_messages 
            )
            response_text = second_response.choices[0].message.content
            print(f"Final response: {response_text}")
        else:
            print("No tool calls found")
            response_text = chat_completion.choices[0].message.content
            print(f"Direct response: {response_text}")
    
    except Exception as e:
        error_message = str(e)
        if "tool choice requires --enable-auto-tool-choice" in error_message:
            print("⚠️ ERROR: Tool calling is not supported by this model.")
            print("The model requires server-side configuration for tool calling.")
            print("Try using a different model or approach.")
        else:
            # For other errors, print the full error message
            print(f"Error: {error_message}")
    
    return response_text

# Define the system prompt with clear instructions about tool usage
system_message = {
    "content": "You are a helpful assistant. You have access to ONLY get_weather function that provides temperature information for locations. ONLY use this function when explicitly asked about weather or temperature. For all other questions, respond directly without using any tools.",
    "role": "system"
}

# Define two different user messages to test
weather_question = {
    "content": "What is the weather like in Paris today?",
    "role": "user"
}

general_question = {
    "content": "Who is the president of the United States?",
    "role": "user"
}

# Initialize the OpenAI compatible CentML client with the API key and base URL
client = OpenAI(api_key=api_key, base_url=base_url)
models = client.models.list()

# Convert the Pydantic models to dictionaries and then to JSON for pretty printing
print("Available Models:")
models_data = []
for model in models:
    # Convert the model to a dictionary
    model_dict = {
        "id": model.id,
        "created": model.created,
        "owned_by": model.owned_by,
        "cost_per_million": f"${model.cost_per_million/100:.2f}",
        "vision_support": model.vision_support
    }
    models_data.append(model_dict)
# Print all models as a single JSON array
print(json.dumps(models_data, indent=4))
print()

# models = [model for model in models if model.id == "deepseek-ai/DeepSeek-R1"]
for model in models:
    print(f"\n--- Testing model: {model.id} ---")
    
    # Test with weather question (should use tool)
    print("\nTesting with weather question:")
    weather_prompt = [system_message, weather_question]
    
    start_time = time.time()
    
    # Process the weather question with tool calling
    response = process_tool_calling(
        client=client,
        model_id=model.id,
        messages=weather_prompt,
        available_functions={"get_weather": get_weather}
    )
    elapsed_time = time.time() - start_time
    print(f"Weather question time taken: {elapsed_time:.2f} seconds")
    
    # Test with general question (should NOT use tool)
    print("\nTesting with general question:")
    general_prompt = [system_message, general_question]
    
    start_time = time.time()

    # For general questions, we'll try without tools
    # Process the weather question with tool calling
    response = process_tool_calling(
        client=client,
        model_id=model.id,
        messages=general_prompt,
        available_functions={"get_weather": get_weather}
    )
    elapsed_time = time.time() - start_time
    print(f"General question time taken: {elapsed_time:.2f} seconds")
