import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env")

client = OpenAI(api_key=api_key)

response = client.responses.create(
    model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
    input="Say hello to my Enterprise AI RAG project."
)

print(response.output_text)