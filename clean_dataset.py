import os
import time
import requests
from io import BytesIO
import easyocr
from duckduckgo_search import DDGS
from PIL import Image

TRAIN_DIR = r"C:\Users\user\OneDrive\Desktop\farmer app\Smart-AI-Farm\dataset\train"
TARGET_NUM = 50

print("Initializing EasyOCR...")
try:
    reader = easyocr.Reader(['en'], gpu=False)
except Exception as e:
    print(f"Failed to load EasyOCR: {e}")
    reader = None

ddgs = DDGS()

def check_text(img_path):
    if reader is None: return False
    try:
        res = reader.readtext(img_path, detail=0)
        return any(len(t.strip()) > 2 for t in res)
    except:
        return True # corrupted, consider it bad

def clean_folder(folder_path):
    # Remove unwanted images and images containing texts
    files = os.listdir(folder_path)
    removed_count = 0
    for f in files:
        f_lower = f.lower()
        filepath = os.path.join(folder_path, f)
        
        # We consider placeholder and sample images as 'unwanted'
        is_unwanted = ('placeholder' in f_lower or 'sample' in f_lower)
        # Check newly downloaded images or 'real_img'
        is_downloaded = ('real_img' in f_lower or 'real_dl' in f_lower)
        
        if is_unwanted:
            try:
                os.remove(filepath)
                removed_count += 1
            except:
                pass
        elif is_downloaded:
            if check_text(filepath):
                print(f"Removed text-containing image: {f}")
                try:
                    os.remove(filepath)
                    removed_count += 1
                except:
                    pass
    return removed_count

def download_real_images(folder_name, folder_path, needed):
    query = folder_name.replace("_", " ") + " agriculture real image"
    print(f"Downloading {needed} images for '{folder_name}'...")
    try:
        # Fetching a larger number of results because some might be invalid or have text
        results = ddgs.images(keywords=query, max_results=needed * 3)
    except Exception as e:
        print(f"Search failed for {folder_name}: {e}")
        return

    saved_count = 0
    for i, res in enumerate(results):
        if saved_count >= needed:
            break
        url = res.get('image')
        if not url: continue
        
        save_path = os.path.join(folder_path, f"real_dl_{int(time.time())}_{i}.jpg")
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(resp.content)
                
                # Check if it is a valid image
                try:
                    img = Image.open(save_path)
                    img.verify()
                except Exception:
                    os.remove(save_path)
                    continue
                
                # Check for text before keeping it
                if check_text(save_path):
                    os.remove(save_path)
                    continue
                
                saved_count += 1
        except Exception:
            if os.path.exists(save_path):
                try: os.remove(save_path)
                except: pass

def main():
    folders = [f for f in os.listdir(TRAIN_DIR) if os.path.isdir(os.path.join(TRAIN_DIR, f))]
    total_folders = len(folders)
    
    for idx, folder in enumerate(folders):
        print(f"[{idx+1}/{total_folders}] Processing folder: {folder}")
        folder_path = os.path.join(TRAIN_DIR, folder)
        
        # Step 1: Clean folder of unwanted or text-containing images
        clean_folder(folder_path)
        
        # Step 2: Add real images based on the file name (folder name)
        current_files = os.listdir(folder_path)
        needed = TARGET_NUM - len(current_files)
        
        if needed > 0:
            download_real_images(folder, folder_path, needed)
            
    print("Dataset cleanup and population based on real images completely finished.")

if __name__ == "__main__":
    main()
