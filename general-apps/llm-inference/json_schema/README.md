
# README: Employee Profile JSON Generator

## Overview

This Python script demonstrates how to use an OpenAI-powered API to generate employee profiles in JSON format that conform to a predefined schema. It uses guided decoding to ensure the generated profiles are schema-compliant and provides validation using the `jsonschema` library.

This example is tailored for testing with CentML’s hosted LLM endpoint, using environment variables for configuration.

## Prerequisites

### Python Environment:
- Ensure you have Python 3.7 or later installed.
- Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

### Environment Variables:
Set the following environment variables before running the script:
```bash
export CENTML_API_KEY="no_key"  # Replace with your API key if available
export CENTML_API_HOSTNAME="llama3-8b.user-1404.gcp.centml.org" # replace with your endpoint url
export CENTML_MODEL_NAME="meta-llama/Meta-Llama-3-8B-Instruct" # replace with your model
```

## How It Works

1. **Schema Definition:**
     - The script defines a JSON schema for employee profiles, including fields like name, age, skills, and work_history.
2. **OpenAI API Interaction:**
     - The script interacts with the CentML-hosted OpenAI-compatible API to generate JSON profiles.
     - The API generates responses based on the schema using guided decoding.
3. **Validation:**
     - Each generated JSON profile is validated against the predefined schema using `jsonschema`.
     - The script ensures that subsequent profiles have unique name and age fields.
4. **Environment Variables:**
     - The script dynamically reads configuration details (API key, hostname, and model name) from environment variables for flexibility.

## Usage Instructions

1. **Set Environment Variables:**
     Export the required environment variables:
     ```bash
     export CENTML_API_KEY="no_key"  # Replace with your API key
     export CENTML_API_HOSTNAME="llama3-8b.user-1404.gcp.centml.org" # replace with your endpoint url
     export CENTML_MODEL_NAME="meta-llama/Meta-Llama-3-8B-Instruct" # replace with your model
     ```

2. **Run the Script:**
     Execute the script to generate and validate employee profiles:
     ```bash
     python main.py
     ```

3. **Output:**
     - The script will generate and print two valid, schema-compliant JSON profiles.
     - Example output:
         ```json
         Generated Profile 1:
         {
                 "name": "Alice Johnson",
                 "age": 28,
                 "skills": ["Python", "SQL", "Leadership"],
                 "work_history": [
                         {"company": "TechCorp", "duration": 3.5, "position": "Software Engineer"},
                         {"company": "DataPros", "duration": 2, "position": "Data Analyst"}
                 ]
         }

         Generated Profile 2:
         {
                 "name": "Bob Smith",
                 "age": 35,
                 "skills": ["Java", "Kotlin", "Teamwork"],
                 "work_history": [
                         {"company": "BuildIt", "duration": 5, "position": "Project Manager"},
                         {"company": "AppSolutions", "duration": 3, "position": "Mobile Developer"}
                 ]
         }
         ```
     Both profiles are valid and unique!

## Key Features

- **Schema Validation:** Ensures all generated JSON profiles adhere to the predefined schema.
- **Guided Decoding:** Uses guided decoding to enforce structure in the generated data.
- **Environment Configurable:** Reads endpoint, API key, and model name from environment variables for flexibility.
- **Error Handling:**
    - Detects and reports schema validation issues.
    - Ensures generated profiles are unique in key fields (name, age).

## Troubleshooting

- **Missing Environment Variables:**
    If environment variables are not set, the script defaults to:
    - API Key: "no_key"
    - Hostname: "llama3-8b.user-1404.gcp.centml.org"
    - Model Name: "meta-llama/Meta-Llama-3-8B-Instruct"
- **JSON Validation Errors:**
    Ensure the schema is correctly defined and matches the expected structure.
- **Network Errors:**
    Confirm that the hostname is reachable and the API key is valid.

## Customization

To adapt the script for other schemas:
1. Update the `sample_json_schema` object with your desired schema.
2. Adjust the prompts in the `messages` array accordingly.

For questions or additional support, feel free to reach out!
```