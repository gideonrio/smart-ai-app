import os
import glob
import cv2
import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor

dataset_dir = r"C:\Users\user\OneDrive\Desktop\farmer app\Smart-AI-Farm\dataset"

def is_infographic_or_poster(img_path):
    """ Fast OpenCV heuristic to detect text-heavy posters or infographics """
    try:
        img = cv2.imread(img_path)
        if img is None:
            return True # Delete corrupt/empty files
            
        h, w = img.shape[:2]
        img_area = h * w
        
        # 1. Unnatural aspect ratio (very tall or exceptionally wide banners)
        aspect_ratio = w / float(h)
        if aspect_ratio < 0.4 or aspect_ratio > 2.5:
            return True
            
        # 2. Heuristic text bounding box detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Use simple edge detection
        edges = cv2.Canny(gray, 100, 200)
        
        # Morphological CLOSE to connect text letters horizontally into blocks
        # 15px wide by 3px high block helps connect adjacent characters
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 3))
        connected = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        # Find contours of connected blocks
        contours, _ = cv2.findContours(connected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        text_area = 0
        box_count = 0
        
        for cnt in contours:
            x, y, box_w, box_h = cv2.boundingRect(cnt)
            # A valid string of text is usually a wide rectangle
            if box_w > 30 and box_h > 10 and box_h < 100:
                if box_w / float(box_h) > 1.5:
                    text_area += (box_w * box_h)
                    box_count += 1
                    
        # If there are > 7 text-like blocks or they eat up > 3% of the image
        if box_count >= 7 or text_area > (img_area * 0.03):
            return True
            
        return False
        
    except Exception as e:
        return False

def check_and_delete(img_path):
    if is_infographic_or_poster(img_path):
        print(f"[CLEANUP] Removing text-heavy/poster image: {os.path.basename(img_path)}")
        try:
            os.remove(img_path)
        except OSError:
            pass # File might be locked or already deleted

def run_cleanup_cycle():
    extensions = ('*.png', '*.jpg', '*.jpeg')
    all_images = []
    
    for subset in ["train", "validation"]:
        subset_dir = os.path.join(dataset_dir, subset)
        if os.path.exists(subset_dir):
            for ext in extensions:
                # Target the real images downloading now
                all_images.extend(glob.glob(os.path.join(subset_dir, "*", f"real_img_{ext}")))
                
    if not all_images:
        return
        
    # Process concurrently using fast cv2
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(check_and_delete, all_images)

if __name__ == "__main__":
    print("Starting cleaner to sweep and remove posters/infographics (Single Sweep)...")
    run_cleanup_cycle()
    print("Cleanup loop finished.")
