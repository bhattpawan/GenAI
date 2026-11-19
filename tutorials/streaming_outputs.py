from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

instructions = "You are a summarises who return answer in 100 words or less"

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI Key not found")

client = OpenAI()

stream = client.responses.create(
    model="gpt-6-luna",
    input="Expplain agentic ai",
    instructions=instructions,
    stream=True,
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)
