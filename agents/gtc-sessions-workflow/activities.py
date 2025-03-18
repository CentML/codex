"""Module for processing and filtering GTC conference sessions based 
on AI/ML system optimization relevance."""

import asyncio
import json
import string
from typing import List, Optional

import aiohttp
import openai
from pydantic import BaseModel
from temporalio import activity

class LLMResponseError(Exception):
    """Raised when the LLM fails to generate a valid response."""

class Prompt(BaseModel):
    """Configuration for LLM prompting."""
    system_prompt: str
    user_prompt_template: str
    model: str

class Session(BaseModel):
    """Represents a GTC conference session with essential metadata."""
    sessionID: str  # Unique identifier for the session
    title: str      # Title of the session
    abstract: str   # Abstract describing the session content

class ProcessSessionsInput(BaseModel):
    """Input model for the process_sessions activity."""
    min_sessions: list[Session]  # Current list of top sessions (sorted by relevance)
    new_sessions: list[Session]  # New sessions to evaluate and potentially add
    api_key: str                 # API key for CentML Serverless API
    prompt: Prompt

class FilterSessionsInput(BaseModel):
    """Input model for the filter_sessions activity."""
    sessions: List[Session]  # List of sessions to filter
    api_key: str             # API key for CentML Serverless API
    prompt: Prompt

async def complete_with_schema(
    api_key: str,
    base_url: str,
    schema: dict,
    system_prompt: str,
    user_prompt: str,
    model: str,
) -> tuple[str, str | None]:
    """
    Performs a LLM completion with a specified JSON schema.

    Constructs a system message incorporating the schema and requests a chat completion
    that adheres to it. Used as a utility for evaluating sessions via natural language processing.

    Args:
        api_key (str): The API key for authenticating with CentML Serverless API.
        base_url (str): The base URL for the CentML Serverless API endpoint.
        schema (dict): JSON schema that the response must follow.
        system_prompt (str): Base system prompt for the AI model.
        user_prompt (str): Specific prompt provided by the user.
        model (str): Model identifier for CentML Serverless API. 
    Returns:
        tuple[str, str | None]: A tuple containing:
            - The response content as a JSON string.
            - Optional reasoning content if provided by the API, else None.

    Raises:
        LLMResponseError: If the API fails to generate a response.
    """
    client = openai.AsyncOpenAI(api_key=api_key, base_url=base_url)
    schema_str = json.dumps(schema)
    system_message = f"{system_prompt} Here's the json schema you need to adhere to: <schema>{schema_str}</schema>"

    response = await client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt},
        ],
        model=model,
        stream=False,
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "response", "schema": schema, "strict": True},
        },
    )

    content = response.choices[0].message.content
    if not content:
        print(response)
        raise LLMResponseError("Failed to generate a response.")

    reasoning = getattr(response.choices[0].message, 'reasoning_content', None)
    return content, reasoning

async def process_session_filter(api_key: str, session: Session, prompt: Prompt) -> bool:
    """Filter a single session based on relevance criteria."""
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"result": {"type": "boolean"}},
        "required": ["result"],
        "additionalProperties": False,
    }
    
    user_prompt = prompt.user_prompt_template.format(
        title=session.title,
        abstract=session.abstract
    )
    
    content, reasoning = await complete_with_schema(
        api_key, "https://api.centml.com/openai/v1", schema, 
        prompt.system_prompt, user_prompt, prompt.model
    )
    
    print("abstract", session.abstract)
    print("filter reasoning", reasoning)
    print("filter content", content)
    obj = json.loads(content)
    return obj["result"]


# Cache for storing comparison results to avoid redundant API calls
cache = {}

async def compare_sessions(api_key: str, a: Session, b: Session, prompt: Prompt) -> int:
    """Compare two sessions to determine which is more relevant."""
    # Generate bidirectional cache keys
    key_ab = f"{a.sessionID}_{b.sessionID}"
    key_ba = f"{b.sessionID}_{a.sessionID}"

    # Check cache to avoid redundant comparisons
    if key_ab in cache:
        print(f"Cache hit for {a.title} vs. {b.title}")
        return cache[key_ab]
    elif key_ba in cache:
        print(f"Cache hit for {b.title} vs. {a.title}")
        return -cache[key_ba]

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {"result": {"type": "integer", "enum": [1, -1]}},
        "required": ["result"],
        "additionalProperties": False,
    }

    user_prompt = prompt.user_prompt_template.format(
        title_a=a.title,
        abstract_a=a.abstract,
        title_b=b.title,
        abstract_b=b.abstract
    )

    print(f"Comparing {a.title} with {b.title}")
    content, reasoning = await complete_with_schema(
        api_key, "https://api.centml.com/openai/v1", schema,
        prompt.system_prompt, user_prompt, prompt.model
    )

    print("reasoning", reasoning)
    print("content", content)
    obj = json.loads(content)
    result = obj["result"]
    cache[key_ab] = result
    return result

class FetchSessionsInput(BaseModel):
    """Input model for the fetch_sessions activity."""
    from_offset: Optional[int]  # Optional offset for pagination, None for initial fetch

@activity.defn
async def fetch_sessions(fetch_sessions_input: FetchSessionsInput) -> List[Session]:
    """
    Fetches sessions from the GTC conference API.

    Sends a POST request to retrieve session data, supporting pagination via an offset.
    Part of a Temporal.io workflow for session processing.

    Args:
        fetch_sessions_input (FetchSessionsInput): Input containing an optional offset.

    Returns:
        List[Session]: List of parsed Session objects from the API response.

    Raises:
        aiohttp.ClientResponseError: If the API request fails.
    """
    from_offset = fetch_sessions_input.from_offset
    url = 'https://events.rainfocus.com/api/search'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.nvidia.com',
        'priority': 'u=1, i',
        'referer': 'https://www.nvidia.com/',
        'rfapiprofileid': 'kPEXqZyAH2yKiQIBjup0YsyR0slBWDne',
        'rfwidgetid': 'DrwI9RRokZ85dwAXIgogWYLFShMaC93k'
    }
    params = {
        "type": "session",
        "browserTimezone": "America/Toronto",
        "catalogDisplay": "list",
    }
    if from_offset is not None:
        params["from"] = str(from_offset)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=params) as response:
            response.raise_for_status()
            obj = await response.json()

    new_sessions: list[Session] = []
    # Response structure differs based on whether it's the initial fetch or paginated
    if from_offset is None:
        for d in obj["sectionList"][0]["items"]:
            new_sessions.append(Session(**d))
    else:
        for d in obj["items"]:
            new_sessions.append(Session(**d))

    return new_sessions

async def async_filter(arr: list, predicate, concurrency: int = 1) -> list:
    """
    Asynchronously filters a list using a predicate function with concurrency.

    Employs multiple worker tasks to evaluate items concurrently, with retry logic for robustness.

    Args:
        arr (list): List of items to filter.
        predicate (callable): Async function returning a boolean for each item.
        concurrency (int, optional): Number of concurrent workers. Defaults to 1.

    Returns:
        list: Filtered list containing items where predicate returned True.
    """
    index = 0
    results: list[bool] = [False] * len(arr)

    async def worker():
        nonlocal index
        while index < len(arr):
            current_index = index
            index += 1
            attempts = 0
            while attempts < 2:  # Retry up to 2 times on failure
                try:
                    results[current_index] = await predicate(arr[current_index])
                    break
                except Exception as error:
                    print(error)
                    print("Retrying item", current_index)
                    attempts += 1
            if attempts == 2:  # Final attempt without retry
                try:
                    results[current_index] = await predicate(arr[current_index])
                except Exception as error:
                    print(error)
                    print("Retrying item", current_index)

    workers = [asyncio.create_task(worker()) for _ in range(concurrency)]
    await asyncio.gather(*workers)
    return [item for idx, item in enumerate(arr) if results[idx]]

@activity.defn
async def filter_sessions(filter_sessions_input: FilterSessionsInput) -> List[Session]:
    """
    Filters sessions for relevance to AI/ML system optimizations.

    Uses concurrent filtering to evaluate sessions against specific criteria via CentML API.
    Part of a Temporal.io workflow.

    Args:
        filter_sessions_input (FilterSessionsInput): Input with sessions and API key.

    Returns:
        List[Session]: Filtered list of relevant sessions.
    """
    filtered_sessions = await async_filter(
        filter_sessions_input.sessions,
        predicate=lambda session: process_session_filter(filter_sessions_input.api_key, session, filter_sessions_input.prompt),
        concurrency=3  # Process 3 sessions concurrently
    )
    return filtered_sessions

async def find_insertion_point(api_key: str, min_sessions: list[Session], new_session: Session, prompt: Prompt) -> int:
    """
    Finds the insertion point for a new session in a sorted list using binary search.

    Assumes min_sessions is sorted in descending order of relevance (best first).
    Uses compare_sessions to maintain order.

    Args:
        api_key (str): API key for CentML Serverless API.
        min_sessions (list[Session]): Sorted list of top sessions.
        new_session (Session): Session to insert.
        prompt (Prompt): Prompt configuration for session comparison.

    Returns:
        int: Index where new_session should be inserted.
    """
    left = 0
    right = len(min_sessions)
    while left < right:
        mid = (left + right) // 2
        if await compare_sessions(api_key, new_session, min_sessions[mid], prompt) == -1:  # new_session > mid
            right = mid
        else:
            left = mid + 1
    return left

@activity.defn
async def process_sessions(input: ProcessSessionsInput) -> List[Session]:
    """Maintains a list of the top 10 most relevant sessions."""
    min_sessions = input.min_sessions
    new_sessions = input.new_sessions
    api_key = input.api_key

    for new_session in new_sessions:
        if len(min_sessions) == 0:
            min_sessions.append(new_session)
        elif len(min_sessions) < 10:
            pos = await find_insertion_point(api_key, min_sessions, new_session, input.prompt)
            min_sessions.insert(pos, new_session)
        else:
            if await compare_sessions(api_key, new_session, min_sessions[-1], input.prompt) == -1:
                pos = await find_insertion_point(api_key, min_sessions, new_session, input.prompt)
                min_sessions.insert(pos, new_session)
                min_sessions.pop(-1)  # Remove least relevant session
    return min_sessions

def contains_non_english_characters(text: str) -> bool:
    """
    Checks if text contains non-English (non-ASCII) characters.

    English characters include ASCII letters, digits, punctuation, and space.

    Args:
        text (str): Text to evaluate.

    Returns:
        bool: True if non-English characters are present, False otherwise.
    """
    english_chars = string.ascii_letters + string.digits + string.punctuation + " "
    return any(char not in english_chars for char in text)

class FilterNonEnglishSessionsInput(BaseModel):
    """Input model for the filter_non_english_sessions activity."""
    sessions: List[Session]  # List of sessions to filter

@activity.defn
async def filter_non_english_sessions(filter_non_english_sessions_input: FilterNonEnglishSessionsInput) -> List[Session]:
    """
    Filters out sessions likely containing non-English text.

    Removes sessions with titles or abstracts containing non-standard characters.
    Part of a Temporal.io workflow.

    Args:
        filter_non_english_sessions_input (FilterNonEnglishSessionsInput): Input with sessions to filter.

    Returns:
        List[Session]: List of sessions likely in English.
    """
    filtered_sessions = [
        session for session in filter_non_english_sessions_input.sessions
        if not (contains_non_english_characters(session.title) or contains_non_english_characters(session.abstract))
    ]
    return filtered_sessions