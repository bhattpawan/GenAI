from google import genai
from pprint import pprint
from dotenv import load_dotenv
import os

load_dotenv()
model = "gemini-3.5-flash-lite"
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError(
        "API key not found. Please set the GOOGLE_API_KEY environment variable."
    )

client = genai.Client(api_key=API_KEY)


def generate_response(user_input, previous_interaction_id=None):
    interaction = client.interactions.create(
        model=model, input=user_input, previous_interaction_id=previous_interaction_id
    )

    interaction_id = interaction.id
    response = interaction.output_text

    return response, interaction_id


def generate_streaming_response(user_input, previous_interaction_id=None):

    print("Bot: ", end="", flush=True)

    stream = client.interactions.create(
        model=model,
        input=user_input,
        previous_interaction_id=previous_interaction_id,
        store=True,
        stream=True,
    )

    interaction_id = None

    for event in stream:

        if event.event_type == "interaction.created":
            interaction_id = event.interaction.id

        elif event.event_type == "step.delta":
            if event.delta.type == "text":
                print(event.delta.text, end="", flush=True)

        elif event.event_type == "interaction.completed":
            interaction_id = event.interaction.id

    print()

    return interaction_id


print("=" * 10)
print("MY CHATBOT")
print("=" * 10)
print("Enter 1 to start a new conversation")
print("Enter 0 to exit")


previous_interaction_id = None

try:
    while True:

        user_input = input("You: ")

        if not user_input.strip():
            print("Please enter a valid input.")
            continue

        if user_input.strip() == "0":
            print("Exiting the chatbot. Goodbye!")
            break
        elif user_input.strip() == "1":
            previous_interaction_id = None
            print("Starting a new conversation...")
            continue

        # response, interaction_id = generate_response(
        #     user_input, previous_interaction_id
        # )
        # print(f"Bot: {response}", flush=True)

        # interaction_id = generate_streaming_response(
        #     user_input, previous_interaction_id
        # )
        # previous_interaction_id = interaction_id

        previous_interaction_id = generate_streaming_response(
            user_input, previous_interaction_id
        )

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
