import os
import base64
import requests
import json

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_plant_with_llama(image_path):
    """
    Attempts to analyze the plant image using Llama Vision.
    First tries Groq API if GROQ_API_KEY is set.
    Falls back to local Ollama if no key or Groq fails.
    Returns a dict with 'part', 'disease', and 'pest', or None if both fail.
    """
    base64_image = encode_image(image_path)
    prompt = 'Analyze this plant image. Reply strictly in JSON format with no markdown formatting: {"part": "leaf/fruit/stem/root/whole plant", "disease": "disease name or Healthy", "pest": "pest name or None"}. If you cannot determine, classify to the best of your ability.'

    # Try Groq API first
    api_key = os.environ.get("GROQ_API_KEY")
    if api_key:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            "temperature": 0.1,
            "max_tokens": 150
        }
        try:
            response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                # clean up potential markdown formatting from Llama
                content = content.replace("```json", "").replace("```", "").strip()
                return json.loads(content)
        except Exception as e:
            print(f"Groq Llama Vision Error: {e}")

    # Fallback to local Ollama (llama3.2-vision)
    ollama_payload = {
        "model": "llama3.2-vision",
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [base64_image]
            }
        ],
        "format": "json",
        "stream": False
    }
    try:
        response = requests.post("http://localhost:11434/api/chat", json=ollama_payload, timeout=15)
        if response.status_code == 200:
            content = response.json()['message']['content']
            content = content.replace("```json", "").replace("```", "").strip()
            return json.loads(content)
    except Exception as e:
        print(f"Local Ollama Vision Error: {e}")

    return None
