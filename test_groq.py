import os
import json
import base64
import httpx
from groq import Groq
import re

GROQ_API_KEY = "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"
client = Groq(
    api_key=GROQ_API_KEY,
    http_client=httpx.Client(proxy=None)
)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Grab a real image from the dataset
train_path = r"C:\Users\user\OneDrive\Desktop\farmer app\Smart-AI-Farm\dataset\train\leaf_tomato_healthy"
images = []
if os.path.exists(train_path):
    images = [os.path.join(train_path, f) for f in os.listdir(train_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

if images:
    temp_path = images[0]
    print(f"Testing with image: {temp_path}")
    base64_image = encode_image(temp_path)
else:
    print("No images found in dataset folder to test with.")
    exit()

prompt = """
Analyze this crop/plant image carefully. Output ONLY a valid JSON object. Do not include any explanations, markdown boundaries, or extra text.

The JSON MUST have the following valid keys and primitive values (examples provided):
- "plant_type": "Tomato"
- "plant_part": "Leaf"
- "disease_pest": "Healthy"
- "confidence": 95.5
- "treatment": "Maintain current schedule."
- "pesticide": "None needed"
"""

try:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0.1
    )
    
    content = chat_completion.choices[0].message.content.strip()
    print("====== RAW GROQ OUTPUT ======")
    print(content)
    print("=============================")
    
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    if json_match:
        json_str = json_match.group(0)
        print("====== EXTRACTED JSON ======")
        print(json_str)
        print("============================")
        result = json.loads(json_str)
        print("SUCCESSFULLY PARSED!")
    else:
        print("FAILED TO MATCH JSON REGEX")

except Exception as e:
    import traceback
    print(traceback.format_exc())
