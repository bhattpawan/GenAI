import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI Key Not Found")

client = OpenAI()

previous_response_id = None

while True:
    query = input("You: ").strip()

    if not query:
        continue

    if query.lower() == "exit":
        break

    try:
        if previous_response_id is None:
            response = client.responses.create(model="gpt-6-luna", input=query)
        else:
            response = client.responses.create(
                model="gpt-6-luna",
                input=query,
                previous_response_id=previous_response_id,
            )

        print(f"Assistant: {response.output_text}")
        previous_response_id = response.id
    except Exception as e:
        print(e)
        break
