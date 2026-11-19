from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI API Key not found")

client = OpenAI()

instructions = """You are helpful assistant who answers user. Keep the answer short an concise within 100 words. Mske sure you do not miss any critical points and always answer as per the level of information asked by the user. Do not hallucinate or make up any information. Just deny if you cannot answer it confidently. """

print("== CHATBOT ==")
print("== RESET to Reset ==")
print("== EXIT to Quit ==")
print("===========================")

previous_response_id = None

while True:

    try:
        user_input = input("You: ").strip()

        if not user_input:
            print("Please enter a valid input")
            continue

        if user_input.lower() == "exit":
            print("== ADIOS!! ==")
            break

        if user_input.lower() == "reset":
            print("== Conversation Reset ==")
            previous_response_id = None
            continue

        if not previous_response_id:
            stream = client.responses.create(
                model="gpt-6-luna",
                instructions=instructions,
                input=user_input,
                stream=True,
            )
        else:
            stream = client.responses.create(
                model="gpt-6-luna",
                instructions=instructions,
                input=user_input,
                stream=True,
                previous_response_id=previous_response_id,
            )

        print("Assistant: ", end="")
        for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)
            elif event.type == "response.completed":
                previous_response_id = event.response.id
        print()

    except Exception as e:
        print(e)
