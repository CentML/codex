from openai import OpenAI
import os
import json
import time

# Supply your API key from https://app.centml.com/user/vault
api_key = os.environ.get("CENTML_API_KEY")
assert api_key is not None, "Please provide an API Key"
base_url = "https://api.centml.com/openai/v1"

# Define the prompt for the OpenAI compatible API
prompt = [
    {
        "content": (
            "You are a helpful assistant that answers in JSON. Here's the json schema you must adhere to:\n"
            "<schema>\n"
            "{'title': 'WirelessAccessPoint', 'type': 'object', 'properties': {'ssid': {'title': 'SSID', 'type': 'string'}, "
            "'securityProtocol': {'title': 'SecurityProtocol', 'type': 'string'}, 'bandwidth': {'title': 'Bandwidth', 'type': 'string'}}, "
            "'required': ['ssid', 'securityProtocol', 'bandwidth']}\n"
            "</schema>\n"
        ),
        "role": "system"
    },
    {
        "content": (
            "The access point's SSID should be 'OfficeNetSecure', it uses WPA2-Enterprise as its security protocol, "
            "and it's capable of a bandwidth of up to 1300 Mbps on the 5 GHz band. This JSON object will be used to document our network "
            "configurations and to automate the setup process for additional access points in the future. Please provide a JSON object that "
            "includes these details."
        ),
        "role": "user"
    }
]

# Define the JSON schema for the wireless access point configuration
schema_json = {
    "title": "WirelessAccessPoint",
    "type": "object",
    "properties": {
        "ssid": {"title": "SSID", "type": "string"},
        "securityProtocol": {"title": "SecurityProtocol", "type": "string"},
        "bandwidth": {"title": "Bandwidth", "type": "integer"}
    },
    "required": ["ssid", "securityProtocol", "bandwidth"]
}

# Initialize the OpenAI compatible CentML client with the API key and base URL
client = OpenAI(api_key=api_key, base_url=base_url)

models = client.models.list()
for model in models:
    print(f"\n--- Testing model: {model.id} ---")
    
    # Time the chat completion call
    start_time = time.time()
    
    # Create a chat completion request with the defined prompt and schema
    chat_completion = client.chat.completions.create(
        model=model.id,
        messages=prompt,
        max_tokens=5000,
        temperature=0,
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "schema", "schema": schema_json}
        }
    )
    
    # Calculate and print the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Time taken: {elapsed_time:.2f} seconds")

    # Pretty print the JSON response
    try:
        json_content = json.loads(chat_completion.choices[0].message.content)
        print("\nJSON response:")
        print(json.dumps(json_content, indent=4, sort_keys=True))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
