import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise KeyError("No OPENAI specific key found")

client = OpenAI()

instructions = """
You are an experienced Data Engineering mentor.

You help users understand:
- Python
- SQL
- PySpark
- Databricks
- Azure data services

Rules:
1. Explain concepts clearly.
2. Use practical examples.
3. Avoid unnecessary jargon.
4. If information is insufficient, say so.
5. Do not invent technical facts.

When explaining a concept, follow this format:

CONCEPT:
Explain the concept.

EXAMPLE:
Provide a practical example.

COMMON MISTAKE:
Explain one common mistake.

INTERVIEW QUESTION:
Provide one relevant interview question.

CONSTRAINTS:

Answer in 100 words or less
"""

print("YOUR DATAENGINEERING MENTOR")
print("Type exit to quit")

while True:
    domain = input("Enter the field you wish to know about: ")
    if not domain.strip():
        print("Please enter a valid domain")
        continue

    if domain.strip() == "exit":
        print("Adios!")
        break

    level = input("Enter the level of expertise Beginner/Intermediate/Advanced: ")

    if not level.strip():
        print("No valid input. Defaulting to Beginner")
        level = "Beginner"

    user_input = f""" Explain about {domain} for a level of {level}. Provide practical examples """

    try:

        response = client.responses.create(
            model="gpt-6-luna", instructions=instructions, input=user_input
        )

        print(response.output_text)

    except Exception as e:
        print("Failure due to below error")
        print(e)
        print("Exiting the process")
        break
