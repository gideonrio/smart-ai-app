from groq import Groq
import httpx
client = Groq(
    api_key="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",
    http_client=httpx.Client(proxy=None)
)
models = client.models.list()
for m in models.data:
    print(m.id)
