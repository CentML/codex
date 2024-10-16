from openai import OpenAI
# Use the environment variable for the API key
centml_api_key = os.getenv("CENTML_API_KEY")  # Ensure the CENTML_API_KEY environment variable is set
if not api_key:
    raise ValueError("CENTML_API_KEY environment variable is not set.")


client = OpenAI(
    api_key=centml_api_key,
    base_url="https://api.centml.com/openai/v1/chat/completions",
)

completion = client.chat.completions.create(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    messages=[{"role":"system","content":"you are helpful"}],
    max_tokens=2000,
    temperature=0.7,
    top_p=1,
    n=1,
    stream=False,
    frequency_penalty=0,
    presence_penalty=0,
    stop=[]
)

print(completion.choices[0].message)