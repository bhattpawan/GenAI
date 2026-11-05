from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
model = "gemini-3.5-flash-lite"

API_KEY = os.getenv("GOOGLE_API_KEY")

SYSTEM_INSTRUCTION = """
You are a helpful assistant.

Rules:
1. Answer all the questions precisely.
2. Do not miss any important points
3. Do not hallucinate, if you do not know something, say so.
"""

generation_config = {"temperature": 0.7, "max_output_tokens": 50}

if not API_KEY:
    raise ValueError(
        "API key not found. Please set the GOOGLE_API_KEY environment variable."
    )

client = genai.Client(api_key=API_KEY)


def get_api_response(input):
    interaction = client.interactions.create(
        model=model,
        input=input,
        system_instruction=SYSTEM_INSTRUCTION,
        generation_config=generation_config,
    )
    return interaction.output_text


def stream_api_response(input):
    stream = client.interactions.create(
        model=model,
        input=input,
        system_instruction=SYSTEM_INSTRUCTION,
        generation_config=generation_config,
        stream=True,
    )
    for event in stream:
        if event.event_type == "step.delta":
            if event.delta.type == "text":
                pprint(event.delta.text)


try:
    user_input = input("Enter your query: ")
    response = get_api_response(user_input)
    print(f"Response: {response}")
    # stream_api_response(user_input)
except Exception as e:
    print(f"An error occurred: {e}")
