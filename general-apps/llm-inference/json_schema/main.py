import re
from openai import OpenAI
import os
import json
import jsonschema


def extract_json_from_response(response):
    """
    Extracts the JSON part from a model response containing additional explanations.
    """
    try:
        # Find the JSON block using a regular expression
        match = re.search(r"```json\n(.*?)```", response, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        # Try to parse the whole response as JSON if no Markdown block is found
        return json.loads(response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to extract JSON from response: {e}")


def generate_employee_profiles():
    # Read configuration from environment variables
    api_key = os.getenv("CENTML_API_KEY", "api-key")  # Default for testing; replace in production
    base_hostname = os.getenv("CENTML_API_HOSTNAME", "qwen-clone.5d87d85b.c-02.centml.com")
    base_url = f"https://{base_hostname}/openai/v1"
    model_name = os.getenv("CENTML_MODEL_NAME", "Qwen/QwQ-32B-Preview")
    guided_decoding_backend = "outlines"

    # Define the JSON schema for an employee profile
    sample_json_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "skills": {"type": "array", "items": {"type": "string", "maxLength": 10}, "minItems": 3},
            "work_history": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "company": {"type": "string"},
                        "duration": {"type": "number"},
                        "position": {"type": "string"},
                    },
                    "required": ["company", "position"],
                },
            },
        },
        "required": ["name", "age", "skills", "work_history"],
    }

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Generate an example JSON for an employee profile that fits this schema: {sample_json_schema}",
        },
    ]

    try:
        client = OpenAI(base_url=base_url, api_key=api_key)

        # Generate the first example
        chat_completion = client.chat.completions.create(
            messages=messages,
            temperature=0,
            max_tokens=1000,
            model=model_name,
            extra_body=dict(
                guided_json=sample_json_schema,
                guided_decoding_backend=guided_decoding_backend,
            ),
        )

        first_response = chat_completion.choices[0].message.content
        print("First Response Content:", first_response)

        # Extract JSON and validate
        profile_1 = extract_json_from_response(first_response)
        jsonschema.validate(instance=profile_1, schema=sample_json_schema)
        print("Generated Profile 1:", json.dumps(profile_1, indent=4))

        # Request another profile with different values
        messages.append({"role": "assistant", "content": first_response})
        messages.append({"role": "user", "content": "Generate another profile with a different name and age."})

        chat_completion = client.chat.completions.create(
            messages=messages,
            temperature=0,
            max_tokens=1000,
            model=model_name,
            extra_body=dict(
                guided_json=sample_json_schema,
                guided_decoding_backend=guided_decoding_backend,
            ),
        )

        second_response = chat_completion.choices[0].message.content
        print("Second Response Content:", second_response)

        # Extract JSON and validate
        profile_2 = extract_json_from_response(second_response)
        jsonschema.validate(instance=profile_2, schema=sample_json_schema)

        # Ensure uniqueness
        if profile_1["name"] == profile_2["name"] or profile_1["age"] == profile_2["age"]:
            raise ValueError("The second profile is not unique. Please check the model's output.")

        print("Generated Profile 2:", json.dumps(profile_2, indent=4))
        print("Both profiles are valid and unique!")

    except jsonschema.exceptions.ValidationError as e:
        print("JSON validation failed:", e.message)
    except ValueError as e:
        print("Error:", e)
    except Exception as e:
        print("An unexpected error occurred:", str(e))


# Run the example
if __name__ == "__main__":
    generate_employee_profiles()