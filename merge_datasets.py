import os
import shutil

BASE_DIR = r"c:\Users\user\OneDrive\Desktop\New folder"
ROOT_DATASET = os.path.join(BASE_DIR, "dataset")
APP_DATASET = os.path.join(BASE_DIR, "Smart-AI-Farm", "dataset")

def merge_folders(src, dst):
    """Recursively merges src folder into dst folder."""
    if not os.path.exists(dst):
        os.makedirs(dst)
    
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            merge_folders(s, d)
        else:
            # Avoid overwriting
            if os.path.exists(d):
                base, ext = os.path.splitext(item)
                counter = 1
                while os.path.exists(os.path.join(dst, f"{base}_{counter}{ext}")):
                    counter += 1
                d = os.path.join(dst, f"{base}_{counter}{ext}")
            shutil.move(s, d)

if os.path.exists(ROOT_DATASET):
    print(f"Merging {ROOT_DATASET} into {APP_DATASET}...")
    # First, handle already organized subfolders in root dataset (train, validation)
    for sub in ['train', 'validation', 'valid']:
        s_path = os.path.join(ROOT_DATASET, sub)
        if os.path.exists(s_path):
            target_sub = 'validation' if sub == 'valid' else sub
            merge_folders(s_path, os.path.join(APP_DATASET, target_sub))
    
    # Next, handle unorganized folders (fruit, leaf, whole_plant) if any left
    sources = ['fruit', 'leaf', 'whole_plant']
    for s in sources:
        src_path = os.path.join(ROOT_DATASET, s)
        if os.path.exists(src_path):
            # These need flat organization
            for root, dirs, files in os.walk(src_path):
                for file in files:
                    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                        rel_path = os.path.relpath(root, ROOT_DATASET)
                        parts = rel_path.split(os.sep)
                        clean_parts = [p.lower() for p in parts if p.lower() not in ['train', 'valid', 'validation', 'test']]
                        class_name = "_".join(clean_parts)
                        
                        is_val = 'valid' in parts or 'validation' in parts
                        target_root = os.path.join(APP_DATASET, 'validation' if is_val else 'train')
                        
                        class_dir = os.path.join(target_root, class_name)
                        os.makedirs(class_dir, exist_ok=True)
                        
                        src_file = os.path.join(root, file)
                        dst_file = os.path.join(class_dir, file)
                        
                        if os.path.exists(dst_file):
                            base, ext = os.path.splitext(file)
                            dst_file = os.path.join(class_dir, f"{base}_{os.urandom(4).hex()}{ext}")
                        
                        shutil.move(src_file, dst_file)
    
    # Cleanup empty root dataset
    shutil.rmtree(ROOT_DATASET)
    print("Dataset combination and cleanup complete.")
else:
    print("Root dataset folder not found. Nothing to merge.")
