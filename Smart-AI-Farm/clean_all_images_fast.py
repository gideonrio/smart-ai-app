import os
import glob
import cv2
import time
from concurrent.futures import ThreadPoolExecutor

dataset_dir = r"C:\Users\user\OneDrive\Desktop\farmer app\Smart-AI-Farm\dataset"

def has_any_text_fast(img_path):
    """
    Ultra-fast heuristic to detect ANY text-like blocks in an image using OpenCV.
    """
    try:
        img = cv2.imread(img_path)
        if img is None:
            return True # Flag corrupt images for deletion
            
        h, w = img.shape[:2]
        
        # Extremely bad aspect ratios (banners/posters)
        aspect = w / float(h) if h > 0 else 0
        if aspect < 0.3 or aspect > 3.0:
            return True
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Stronger edges for text
        edges = cv2.Canny(gray, 100, 200)
        
        # Connect characters
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 4))
        connected = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(connected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        text_blocks = 0
        for cnt in contours:
            x, y, box_w, box_h = cv2.boundingRect(cnt)
            # A valid string of text is at least 30px wide, and not too tall
            if box_w > 30 and 10 < box_h < 100:
                if box_w / float(box_h) > 1.5:
                    text_blocks += 1
                    
        # If we detect ANY solid text blocks (e.g., 2+ characters connected), consider it text
        if text_blocks >= 1:
            return True
            
        return False
    except Exception:
        return False

def check_and_delete(img_path):
    if has_any_text_fast(img_path):
        print(f"[CLEANUP] Removing text image: {os.path.basename(img_path)}")
        try:
            os.remove(img_path)
        except OSError:
            pass

def sweep():
    extensions = ('*.png', '*.jpg', '*.jpeg', '*.webp')
    all_images = []
    
    print(f"Scanning directory: {dataset_dir}")
    for root, _, files in os.walk(dataset_dir):
        for ext in extensions:
            pattern = os.path.join(root, ext)
            all_images.extend(glob.glob(pattern))
            
    if not all_images:
        print("No images found.")
        return
        
    print(f"Found {len(all_images)} images. Starting fast text detection sweep...")
    
    start = time.time()
    with ThreadPoolExecutor(max_workers=12) as executor:
        executor.map(check_and_delete, all_images)
    end = time.time()
    
    print(f"Finished sweeping {len(all_images)} images in {end - start:.2f} seconds.")

if __name__ == "__main__":
    sweep()
