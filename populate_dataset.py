import os
from PIL import Image

train_path = r'C:\Users\user\OneDrive\Desktop\farmer app\Smart-AI-Farm\dataset\train'

# Simple script to ensure every training folder has at least one image
# This allows the app to 'see' the categories

for folder in os.listdir(train_path):
    folder_path = os.path.join(train_path, folder)
    if os.path.isdir(folder_path):
        # Check if already has images
        files = os.listdir(folder_path)
        if not files:
            print(f"Populating empty folder: {folder}")
            # Create a simple 224x224 placeholder image
            # Color based on name
            color = (46, 204, 113) if "healthy" in folder.lower() else (231, 76, 60)
            img = Image.new('RGB', (224, 224), color=color)
            img.save(os.path.join(folder_path, "placeholder.png"))

print("Done populating dataset.")
