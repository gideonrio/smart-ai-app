import os
import glob
from concurrent.futures import ThreadPoolExecutor
import easyocr
import time
from PIL import Image
import warnings

warnings.filterwarnings('ignore') # ignore torch CPU warnings

try:
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)
except Exception as e:
    print(f"Warning: EasyOCR failed to build. {e}")
    reader = None

dataset_dir = r"C:\Users\user\OneDrive\Desktop\farmer app\Smart-AI-Farm\dataset"

def process_image(img_path):
    try:
        if not os.path.exists(img_path): 
            return
            
        # 1. Aspect Ratio Filter (Catches extreme vertical posters like reels/shorts, and banners)
        with Image.open(img_path) as img:
            w, h = img.size
            if h <= 0: return
            aspect_ratio = w / float(h)
            
            if aspect_ratio < 0.6 or aspect_ratio > 2.0:
                print(f"[CLEANUP] Removed {os.path.basename(img_path)} - Suspicious banner/poster aspect ratio ({aspect_ratio:.2f})")
                
                # Pillow locks the file on Windows until img.close(), context manager handles this
        
        # We need to make sure the file is fully closed by PIL before deletion!
        if aspect_ratio < 0.6 or aspect_ratio > 2.0:
            os.remove(img_path)
            return

        # 2. EasyOCR Text Detection Filter (Catches square stock photos with heavy text overlays)
        if reader is not None:
            results = reader.readtext(img_path, detail=1, text_threshold=0.6, low_text=0.4)
            
            word_count = len(results)
            text_area = 0
            img_area = w * h
            
            for (bbox, text, prob) in results:
                if prob > 0.2:
                    (tl, tr, br, bl) = bbox
                    box_w = max(abs(tr[0] - tl[0]), abs(br[0] - bl[0]))
                    box_h = max(abs(bl[1] - tl[1]), abs(br[1] - tr[1]))
                    text_area += (box_w * box_h)

            # Heuristic: 8+ words or massive text block means it's an infographic/poster
            if word_count > 7 or text_area > (img_area * 0.05):
                print(f"[CLEANUP] Removed {os.path.basename(img_path)} - Infographic Detected ({word_count} text blocks, {100*text_area/img_area:.1f}% area)")
                os.remove(img_path)
                
    except Exception as e:
        pass # Corrupt image or locking error, skip gracefully

def sweep():
    extensions = ('*.png', '*.jpg', '*.jpeg')
    all_images = []
    
    for subset in ["train", "validation"]:
        subset_dir = os.path.join(dataset_dir, subset)
        if os.path.exists(subset_dir):
            for ext in extensions:
                all_images.extend(glob.glob(os.path.join(subset_dir, "*", f"real_img_{ext}")))
                
    if not all_images:
        return
        
    print(f"Sweeping {len(all_images)} currently downloaded images for infographics...")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_image, all_images)


if __name__ == "__main__":
    print("Starting deep infographic/poster cleaner script (Single Sweep)...")
    sweep()
    print("Cleanup cycle finished.")
