from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

instructions = """
You are a Data Engineering incident classifier.

Classify incidents into one of these categories:
- DATA_QUALITY
- PIPELINE_FAILURE
- PERFORMANCE
- ACCESS_ISSUE

Follow these examples.

Example:
Incident: Duplicate records appeared in the customer table.
Category: DATA_QUALITY

Example:
Incident: The Databricks job failed because the cluster terminated.
Category: PIPELINE_FAILURE

Example:
Incident: The SQL query takes 40 minutes to complete.
Category: PERFORMANCE

Example:
Incident: The user cannot access the storage account.
Category: ACCESS_ISSUE

Return only the category.
"""

while True:
    incident = input("Incident: ").strip()

    if incident.lower() == "exit":
        break

    if not incident:
        continue

    response = client.responses.create(
        model="gpt-6-luna", instructions=instructions, input=incident
    )

    print(f"Category: {response.output_text}")
