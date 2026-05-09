import os
import shutil

BASE_DIR = r"c:\Users\user\OneDrive\Desktop\New folder"
ROOT_DATASET = os.path.join(BASE_DIR, "dataset")
APP_DATASET = os.path.join(BASE_DIR, "Smart-AI-Farm", "dataset")

def organize_and_move(source_dir, target_base):
    if not os.path.exists(source_dir):
        return
    
    print(f"Processing {source_dir}...")
    for root, dirs, files in os.walk(source_dir):
        # Skip the target directory if it's inside the source (shouldn't be here but just in case)
        if APP_DATASET in root:
            continue
            
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                src_file = os.path.join(root, file)
                
                # Determine class name and target subfolder (train/validation)
                rel_path = os.path.relpath(root, ROOT_DATASET)
                parts = rel_path.split(os.sep)
                
                # Clean up parts to build class name
                # e.g., dataset/train/leaf_tomato_healthy -> leaf_tomato_healthy
                # e.g., dataset/fruit/tomato/train/Bacterial_Spot -> fruit_tomato_bacterial_spot
                clean_parts = [p.lower() for p in parts if p.lower() not in ['train', 'valid', 'validation', 'test', 'dataset']]
                class_name = "_".join(clean_parts)
                
                # Default to train unless 'valid' or 'validation' is in path
                is_val = any(v in [p.lower() for p in parts] for v in ['valid', 'validation'])
                target_sub = 'validation' if is_val else 'train'
                
                target_dir = os.path.join(APP_DATASET, target_sub, class_name)
                os.makedirs(target_dir, exist_ok=True)
                
                dst_file = os.path.join(target_dir, file)
                if os.path.exists(dst_file):
                    base, ext = os.path.splitext(file)
                    dst_file = os.path.join(target_dir, f"{base}_{os.urandom(4).hex()}{ext}")
                
                try:
                    shutil.move(src_file, dst_file)
                except Exception as e:
                    print(f"Error moving {src_file}: {e}")

if os.path.exists(ROOT_DATASET):
    organize_and_move(ROOT_DATASET, APP_DATASET)
    
    # Second pass: cleanup empty directories in root dataset
    print("Cleaning up empty directories...")
    # Walk bottom-up to remove empty dirs
    for root, dirs, files in os.walk(ROOT_DATASET, topdown=False):
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                os.rmdir(dir_path)
            except OSError:
                pass # Not empty
    
    # Try to remove root dataset if empty
    try:
        os.rmdir(ROOT_DATASET)
    except OSError:
        print("Root dataset not empty, keeping it for now.")

print("Consolidation complete.")
