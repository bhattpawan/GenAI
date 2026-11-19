import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI Key Not Found")

client = OpenAI()

history = []

print("Basic Conversational Chatbot")
print("Type reset to reset conversation")
print("Type exit to finish conversation")

while True:

    user_input = input("You: ")
    if not user_input.strip():
        print("Enter a valid input")
        continue

    if user_input.strip().lower() == "exit":
        print("Adios")
        break

    if user_input.strip().lower() == "reset":
        print("Conversation has been reset")
        history = []

    history.append({"role": "user", "content": user_input})

    response = client.responses.create(model="gpt-6-luna", input=history)

    print(f"Assistant: {response.output_text}")

    history.append({"role": "assistant", "content": response.output_text})
