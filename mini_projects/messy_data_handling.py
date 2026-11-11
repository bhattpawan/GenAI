from ollama import chat
from pydantic import BaseModel
from typing import List, Optional

user_input = """
Product SKU P1001 generated revenue of 45K
in January from 150 units.

During February, revenue increased to 60,000
with 200 units sold.

March had 75K in revenue, but the number
of units sold wasn't reported.
"""
user_message = {"role": "user", "content": user_input}

system_message = {
    "role": "system",
    "content": "Extract sales information from the provided text. Any value which has K or thousand, make them as numeric values. Do not add any missing numeric details. Return only the data provided in the input and consider nulls as 0 for numeric values.",
}

messages = [system_message, user_message]


class MonthlySales(BaseModel):
    month: str
    sales: Optional[float]
    units: Optional[int]


class SalesExtraction(BaseModel):
    sku: str
    monthly_sales_data: List[MonthlySales]


response = chat(
    model="gemma4:e4b",
    messages=messages,
    format=SalesExtraction.model_json_schema(),
    think=False,
)

result = SalesExtraction.model_validate_json(response.message.content)

total_sales = 0
total_units = 0

monthly_asp = {}

for item in result.monthly_sales_data:

    if item.sales != 0:
        total_sales += item.sales

    if item.units != 0:
        total_units += item.units

    if item.sales != 0 and item.units != 0:
        monthly_asp[item.month] = item.sales / item.units

print(f"SKU: {result.sku}")
print(f"Total Sales: {total_sales}")
print(f"Total Units: {total_units}")
print(f"Monthly ASP: {monthly_asp}")
