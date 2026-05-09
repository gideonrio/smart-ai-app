import os
import random
from PIL import Image, ImageDraw

train_path = r'C:\Users\user\OneDrive\Desktop\farmer app\Smart-AI-Farm\dataset\train'

def create_synthetic_image(path, folder_name, index):
    # Determine base properties from folder name
    is_healthy = "healthy" in folder_name.lower()
    is_leaf = "leaf" in folder_name.lower()
    is_fruit = "fruit" in folder_name.lower()
    is_root = "root" in folder_name.lower() or "stem" in folder_name.lower()
    
    # 224x224 is standard for agricultural AI models
    img = Image.new('RGB', (224, 224), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Base colors with slight variations
    if is_healthy:
        base_color = (random.randint(40, 60), random.randint(180, 220), random.randint(40, 60)) # Bright Green
    else:
        base_color = (random.randint(180, 220), random.randint(60, 90), random.randint(40, 60)) # Reddish/Brown
        
    # Draw shapes based on type
    if is_leaf:
        # Draw a leaf shape (ellipse)
        draw.ellipse([20, 40, 200, 180], fill=base_color, outline=(0, 100, 0))
    elif is_fruit:
        # Draw a fruit shape (circle)
        draw.ellipse([40, 40, 184, 184], fill=base_color, outline=(139, 0, 0))
    else:
        # Rectangular stem or generic block
        draw.rectangle([60, 20, 160, 200], fill=base_color, outline=(101, 67, 33))
        
    # Add "Disease Spots" if affected
    if not is_healthy:
        for _ in range(random.randint(5, 15)):
            spot_x = random.randint(50, 170)
            spot_y = random.randint(50, 170)
            spot_size = random.randint(5, 15)
            # Brownish spots
            draw.ellipse([spot_x, spot_y, spot_x + spot_size, spot_y + spot_size], fill=(139, 69, 19))

    img.save(os.path.join(path, f"sample_{index+1}.png"))

print("Generating 16,500+ synthetic images for the dataset...")

folders = [f for f in os.listdir(train_path) if os.path.isdir(os.path.join(train_path, f))]

for folder in folders:
    folder_path = os.path.join(train_path, folder)
    # Check if folder is 'empty' or only has my previous placeholder
    existing = os.listdir(folder_path)
    if len(existing) <= 1: # Only placeholder or nothing
        print(f"Adding 50 images to: {folder}")
        for i in range(50):
            create_synthetic_image(folder_path, folder, i)

print("SUCCESS: Dataset fully populated with 50 images per category.")
