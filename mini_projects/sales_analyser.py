import os
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pprint import pprint

load_dotenv()
model = "gemini-3.5-flash-lite"

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError(
        "API key not found. Please set the GOOGLE_API_KEY environment variable."
    )

client = genai.Client(api_key=API_KEY)

SYSTEM_INSTRUCTION = """ You are a sales analysis assistant whose job is to analyze the sales data provided by the user and give the appropriate response. """


class SalesAnalysis(BaseModel):
    sku: str
    total_sales: float
    total_units: int
    monthly_asp: dict[str, float]
    highest_sales_month: str


def read_block():
    print("Enter sales details, then press Enter on an empty line:")
    lines = []
    while True:
        line = input()
        if not line.strip():
            break
        lines.append(line)
    return "\n".join(lines)


user_input = read_block()

interaction = client.interactions.create(
    model=model,
    input=user_input,
    system_instruction=SYSTEM_INSTRUCTION,
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": SalesAnalysis.model_json_schema(),
    },
)

response = SalesAnalysis.model_validate_json(interaction.output_text)

pprint("Response: ", response)
