import traceback
from groq import Groq
client = Groq(api_key="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")
models = ["llama-3.2-11b-vision-preview", "llama-3.3-70b-versatile"]
with open("res.txt", "w", encoding="utf-8") as f:
    for model in models:
        try:
            response = client.chat.completions.create(
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What's in this image?"},
                        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,/9j/4AAQSkZJRg=="}}
                    ]
                }],
                model=model,
                temperature=0.1
            )
            f.write(f"{model} : SUCCESS\n")
        except Exception as e:
            f.write(f"{model} : FAILED - {type(e).__name__} {e}\n")
