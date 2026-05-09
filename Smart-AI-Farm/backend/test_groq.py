import os
import httpx
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

client = Groq(
    api_key=GROQ_API_KEY,
    http_client=httpx.Client(proxy=None)
)

try:
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "Hello, please reply in json: {\"reply\": \"...\"}"}],
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=600,
        response_format={"type": "json_object"}
    )
    print(chat_completion.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
