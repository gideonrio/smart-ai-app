import os
import shutil

BASE_DIR = r"c:\Users\user\OneDrive\Desktop\New folder"
DATASET_SOURCE_DIR = os.path.join(BASE_DIR, "dataset")
TARGET_TRAIN_DIR = os.path.join(DATASET_SOURCE_DIR, "train")
TARGET_VAL_DIR = os.path.join(DATASET_SOURCE_DIR, "validation")

os.makedirs(TARGET_TRAIN_DIR, exist_ok=True)
os.makedirs(TARGET_VAL_DIR, exist_ok=True)

def move_and_organize(source_path, category_name):
    """Moves images from nested folders into a flat structure for training."""
    if not os.path.exists(source_path):
        return
    
    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Create a class name based on the folder path
                # e.g., leaf/train/tomato/Bacterial_Spot -> leaf_tomato_bacterial_spot
                rel_path = os.path.relpath(root, DATASET_SOURCE_DIR)
                parts = rel_path.split(os.sep)
                
                # Cleanup parts
                clean_parts = [p.lower() for p in parts if p.lower() not in ['train', 'valid', 'validation', 'test']]
                class_name = "_".join(clean_parts)
                
                # Identify if it should go to train or validation
                is_val = 'valid' in parts or 'validation' in parts
                target_root = TARGET_VAL_DIR if is_val else TARGET_TRAIN_DIR
                
                class_dir = os.path.join(target_root, class_name)
                os.makedirs(class_dir, exist_ok=True)
                
                # Move file
                src_file = os.path.join(root, file)
                dst_file = os.path.join(class_dir, file)
                
                # Avoid collision
                counter = 1
                base, ext = os.path.splitext(file)
                while os.path.exists(dst_file):
                    dst_file = os.path.join(class_dir, f"{base}_{counter}{ext}")
                    counter += 1
                
                try:
                    shutil.move(src_file, dst_file)
                except Exception as e:
                    print(f"Error moving {src_file}: {e}")

# Source folders provided by user
sources = ['fruit', 'leaf', 'whole_plant']

for s in sources:
    move_and_organize(os.path.join(DATASET_SOURCE_DIR, s), s)

# Finally, cleanup empty old directories
for s in sources:
    path = os.path.join(DATASET_SOURCE_DIR, s)
    if os.path.exists(path):
        shutil.rmtree(path)

print("Dataset organization complete.")
