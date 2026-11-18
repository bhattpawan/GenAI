import os
from dotenv import load_dotenv
from openai import OpenAI, APIError, APIConnectionError, RateLimitError

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Data Engineering Assistant")
print("Type 'exit' to quit.\n")

while True:
    query = input("You: ")
    if not query.strip():
        print("Please enter a valid input")
        continue
    if query.strip().lower() == "exit":
        print(f"Bot: Adios!")
        break
    try:
        response = client.responses.create(
            model="gpt-6-luna",
            instructions="""
                You are a senior Data Engineering assistant.
                Help users with Python, SQL, PySpark and Databricks.
                Explain concepts with practical examples.
                """,
            input=query,
        )
        print(f"Bot: {response.output_text}")
    except RateLimitError:
        print("Bot: API rate limit or quota exceeded.")

    except APIConnectionError:
        print("Bot: Unable to connect to OpenAI.")

    except APIError as e:
        print(f"Bot: OpenAI API error: {e}")
