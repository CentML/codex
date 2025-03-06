import os
import time
import json
import tiktoken 
from openai import OpenAI

def measure_llm_performance():
    """
    Measure the performance of an LLM response using streamed data, adhering to principles of
    reproducibility, transparency, and accuracy as outlined in the Artificial Analysis Methodology.
    """

    
    api_key = os.getenv("CENTML_API_KEY", "replace-with-key")
    base_hostname = os.getenv("CENTML_API_HOSTNAME", "api.centml.com") 
    base_url = f"https://{base_hostname}/openai/v1"
    model_name = os.getenv("CENTML_MODEL_NAME", "deepseek-ai/DeepSeek-R1")
    guided_decoding_backend = "outlines"

    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": (
                "overview of quantum mechanics"
            )
        },
    ]

   
    try:
        enc = tiktoken.get_encoding("cl100k_base") 
    except Exception as e:
        raise RuntimeError("Unable to initialize tokenizer. Please verify the tokenizer name.") from e

   
    prompt_tokens = sum(len(enc.encode(msg["content"])) for msg in messages)

    try:
       
        client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

        
        start_time = time.time()
        total_response_tokens = 0
        first_token_received = False
        first_token_time = None

        
        response_stream = client.chat.completions.create(
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
            model=model_name,
            stream=True,  
        )

        print("### Streaming Response ###")
        for chunk in response_stream:  
            delta = chunk.choices[0].delta
            if hasattr(delta, 'content') and delta.content:
                if not first_token_received:
                    first_token_received = True
                    first_token_time = time.time()
                print(delta.content, end="", flush=True)  
                total_response_tokens += len(enc.encode(delta.content))  

        print("\n### End of Stream ###")
        end_time = time.time()

        
        total_tokens = prompt_tokens + total_response_tokens
        elapsed_time = end_time - start_time
        if first_token_time:
            ttft = first_token_time - start_time
            output_speed = total_response_tokens / (end_time - first_token_time)
            total_response_time_100_tokens = ttft + (100 / output_speed)
        else:
            ttft = None
            output_speed = None
            total_response_time_100_tokens = None

        
        print("\n### Experiment Results ###")
        print("Prompt Messages:\n", json.dumps(messages, indent=4))
        print("\nPerformance Metrics:")
        print(f"Prompt Tokens: {prompt_tokens}")
        print(f"Response Tokens: {total_response_tokens}")
        print(f"Total Tokens: {total_tokens}")
        print(f"Elapsed Time: {elapsed_time:.2f} seconds")
        if ttft is not None:
            print(f"Time to First Token (TTFT): {ttft:.2f} seconds")
            print(f"Output Speed: {output_speed:.2f} tokens/second")
            print(f"Total Response Time for 100 Output Tokens: {total_response_time_100_tokens:.2f} seconds")
        else:
            print("Time to First Token (TTFT): Not available")
            print("Output Speed: Not available")
            print("Total Response Time for 100 Output Tokens: Not available")

    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    print("### Running LLM Performance Measurement Script ###")
    print(f"Model Name: {os.getenv('CENTML_MODEL_NAME', 'Not Specified')}")
    print(f"Base Hostname: {os.getenv('CENTML_API_HOSTNAME', 'Not Specified')}")
    print(f"API Key Provided: {'Yes' if os.getenv('CENTML_API_KEY') else 'No'}")
    measure_llm_performance()