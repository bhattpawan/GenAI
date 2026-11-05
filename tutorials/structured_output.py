import os
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()
model = "gemini-3.5-flash-lite"

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError(
        "API key not found. Please set the GOOGLE_API_KEY environment variable."
    )

client = genai.Client(api_key=API_KEY)


class FeedbackAnalysis(BaseModel):
    sentiment: Literal["positive", "negative", "neutral"]
    delivery_issue: bool
    product_quality: Literal["good", "bad", "average"]
    summary: str


SYSTEM_INSTRUCTION = """ You are a feedback analysis assisstant whose job is to analyse the feedback provided by the user and give the appropriate response. """

user_input = input("Enter your feedback: ")

interaction = client.interactions.create(
    model=model,
    input=user_input,
    system_instruction=SYSTEM_INSTRUCTION,
    response_format={
        "type": "text",
        "mime_type": "application/json",
        "schema": FeedbackAnalysis.model_json_schema(),
    },
)

print("Response: ", interaction.output_text)

response = FeedbackAnalysis.model_validate_json(interaction.output_text)
