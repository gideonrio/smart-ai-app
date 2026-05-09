import os
import httpx
from groq import Groq

# Use the key provided by the user
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

client = Groq(
    api_key=GROQ_API_KEY,
    http_client=httpx.Client(proxy=None)
)

try:
    print("Listing models...")
    models = client.models.list()
    for m in models.data:
        if "vision" in m.id.lower():
            print(f"VISION MODEL: {m.id}")
        else:
            print(f"MODEL: {m.id}")
except Exception as e:
    print(f"ERROR: {e}")
