from ollama import chat
from pydantic import BaseModel
from typing import List, Optional


class MonthlySales(BaseModel):
    month: str
    sales: Optional[float]
    units: Optional[int]


class SalesExtraction(BaseModel):
    sku: str
    monthly_data: List[MonthlySales]


user_input = """
Product ABC123 had sales of 50K in Jan with 250 units.
Feb sales were around 72 thousand and units sold were 300.
In March, we sold 200 units, generating revenue of 60,000.
"""

system_message = {
    "role": "system",
    "content": """
            Extract sales information from the provided text.
            Convert K and thousand into numeric values.
            Do not invent missing values.
            Use null when information is unavailable.
            Return only information supported by the input.
            """,
}

user_message = {"role": "user", "content": user_input}

messages = [system_message, user_message]

response = chat(
    model="qwen3:1.7b",
    messages=messages,
    format=SalesExtraction.model_json_schema(),
    think=False,
)

result = SalesExtraction.model_validate_json(response.message.content)

print(result)
