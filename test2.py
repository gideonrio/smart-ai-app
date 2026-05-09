import os
import requests

url = "http://127.0.0.1:5000/api/predict"

images = []
if os.path.exists("Smart-AI-Farm/dataset"):
    images = [os.path.join("Smart-AI-Farm/dataset", f) for f in os.listdir("Smart-AI-Farm/dataset") if f.endswith(('.jpg', '.png', '.jpeg'))]

if not images:
    print("No images to test.")
    exit()

img_path = images[0]
print(f"Testing API with {img_path}...")

with open(img_path, 'rb') as f:
    files = {'image': f}
    response = requests.post(url, files=files)

print("Status Code:", response.status_code)
print("Response JSON:", response.text)
