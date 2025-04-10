import concurrent.futures
import gradio as gr
from openai import OpenAI
import requests
import json
import random
from datetime import datetime
import os

# Remove the hardcoded client configuration
# Configure the OpenAI client for centml.
client = None  # Will be initialized with user provided API key

RESULTS_FILE = "arena_votes.json"

# Fetch model names from the centml API.
def fetch_models():
    try:
        models = client.models.list()
        print("Available models:", models.data)
        return models.data
    except Exception as e:
        print("Error fetching models:", e)
        # Fallback list if the fetch fails.
        return [
            "deepseek-ai/DeepSeek-V3-0324",
            "meta-llama/Llama-3.2-3B-Instruct",
            "deepseek-ai/DeepSeek-R1",
            "Qwen/QwQ-32B",
            "Qwen/Qwen2.5-VL-7B-Instruct",
            "meta-llama/Llama-3.3-70B-Instruct",
            "microsoft/Phi-4-mini-instruct"
        ]

# Get a model response using centml's OpenAI-compatible API.
def get_model_response(prompt, model_name):
    try:
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7,
            top_p=1,
            n=1,
            stream=False,
            frequency_penalty=0,
            presence_penalty=0.5,
            stop=[]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error from {model_name}: {str(e)}"

def get_single_response(args):
    """Helper function to handle single model response"""
    idx, model, prompt = args  # Properly unpack all three values
    try:
        response = get_model_response(prompt, model.id)
        return {
            "option": f"Option {idx+1}",
            "model": model.id,
            "response": response
        }
    except Exception as e:
        return {
            "option": f"Option {idx+1}",
            "model": model.id,
            "response": f"Error: {str(e)}"
        }

def generate_outputs(prompt):
    models = fetch_models()
    outputs = []
    
    # Create arguments list for parallel processing
    args = [(idx, model, prompt) for idx, model in enumerate(models)]
    
    # Use ThreadPoolExecutor for parallel requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(models)) as executor:
        try:
            # Submit all requests in parallel
            futures = [executor.submit(get_single_response, arg) for arg in args]
            
            # Collect and shuffle just the model responses
            responses = []
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                responses.append(result)
            
            # Shuffle responses but maintain ordered options
            random.shuffle(responses)
            
            # Reassign option numbers in order
            for idx, response in enumerate(responses):
                response["option"] = f"Option {idx + 1}"
                outputs.append(response)
                
        except Exception as e:
            print(f"Error in parallel execution: {e}")
    
    # Return ordered options with shuffled responses
    if outputs:
        return outputs, [f"Option {i+1}" for i in range(len(outputs))]
    else:
        return [], []

# Record the vote by updating (or creating) a JSON results file.
def record_vote(prompt, outputs_json, selected_option):
    outputs = json.loads(outputs_json)
    voted_output = next((out for out in outputs if out["option"] == selected_option), None)
    if not voted_output:
        return "Invalid selection. Vote not recorded."
    voted_model = voted_output["model"]

    # Load existing results or create new.
    try:
        with open(RESULTS_FILE, "r") as f:
            results = json.load(f)
    except FileNotFoundError:
        results = {}

    if voted_model not in results:
        results[voted_model] = {"votes": 0, "history": []}
    
    results[voted_model]["votes"] += 1
    results[voted_model]["history"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "response": voted_output["response"]
    })

    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)
    
    return f"Vote recorded for model: {voted_model}"

# Build the Gradio interface with improved layout
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🤖 LLM Arena
    ## Compare Model Outputs and Vote for the Best Response
    """)
    
    # Add API key input at the top
    with gr.Row():
        with gr.Column():
            api_key_input = gr.Textbox(
                label="CentML API Key",
                placeholder="",
                type="password",  # Makes the input secure
                value=os.getenv("CENTML_API_KEY", "")  # Use environment variable if available
            )
    
    with gr.Row():
        with gr.Column(scale=4):
            prompt_input = gr.Textbox(
                label="Your Prompt",
                placeholder="Type your prompt here...",
                lines=3
            )
        with gr.Column(scale=1):
            generate_button = gr.Button("Generate Responses", variant="primary")
    
    # Add progress indicator
    status_text = gr.Markdown("", elem_id="status")

    # Container for model outputs using Column for separation
    output_boxes = []
    for i in range(10):  # Adjust based on number of models
        with gr.Row():
            with gr.Column():
                with gr.Group(visible=True) as group:
                    gr.Markdown(f"### Option {i+1}")
                    output_box = gr.Markdown(
                        value="",
                        visible=False,
                        elem_classes=["output-box"]
                    )
                    output_boxes.append(output_box)
    
    # Add custom CSS for better spacing and borders
    gr.HTML("""
        <style>
        .output-box {
            border: 1px solid #444;
            border-radius: 8px;
            padding: 16px;
            margin: 8px 0;
            background: #1a1a1a;
        }
        .group {
            margin-bottom: 24px;
        }
        </style>
    """)
    
    with gr.Row():
        with gr.Column():
            vote_radio = gr.Radio(
                choices=[], 
                label="💫 Select the response you think is best",
                interactive=True
            )
    
    with gr.Row():
        with gr.Column():
            vote_button = gr.Button("Cast Your Vote", variant="secondary")
            vote_result = gr.Markdown()
    
    outputs_state = gr.State()

    def on_generate(api_key, prompt):
        try:
            # Initialize client with provided API key
            global client
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.centml.com/openai/v1",
            )
            
            # Generate outputs first
            outputs, _ = generate_outputs(prompt)
            # Recompute options based on the number of responses
            options = [f"Option {i+1}" for i in range(len(outputs))]
            
            # Initialize results array for all components
            results = []
            
            # Add status text
            results.append("🔄 Processing responses...")
            
            # Update each output box in order
            for i in range(len(output_boxes)):
                if i < len(outputs):
                    results.append(gr.update(
                        value=outputs[i]["response"],
                        visible=True
                    ))
                else:
                    results.append(gr.update(value="", visible=False))
            
            # Update radio choices to use only the valid options
            results.extend([
                gr.update(choices=options, value=None),  # Update radio with correct number of options
                json.dumps(outputs),                     # State
                "✅ Generation complete!"                # Final status
            ])
            
            return results
        except Exception as e:
            # Handle error case with correct number of outputs
            error_results = [f"Error: {str(e)}"]  # Status
            error_results.extend([gr.update(visible=False)] * len(output_boxes))  # Outputs
            error_results.extend([
                gr.update(choices=[], value=None),  # Radio
                "[]",                               # State
                "API Key or Generation Failed!"     # Final status
            ])
            return error_results

    # Update the click handler to include the API key
    generate_button.click(
        on_generate,
        inputs=[api_key_input, prompt_input],
        outputs=[status_text] + output_boxes + [vote_radio, outputs_state, vote_result],
        show_progress=True
    )
    
    vote_button.click(
        record_vote,
        inputs=[prompt_input, outputs_state, vote_radio],
        outputs=vote_result
    )

demo.launch(share=True, debug=True)