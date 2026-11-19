from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI API Key not found")

client = OpenAI()

instructions = "You are hwlpful assistant who answers user"