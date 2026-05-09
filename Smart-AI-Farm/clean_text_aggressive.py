import os
import glob
from concurrent.futures import ThreadPoolExecutor
import easyocr
import time
from PIL import Image
import warnings

# Suppress warnings
warnings.filterwarnings('ignore')

try:
    # Initialize reader for English. GPU=False for compatibility if no CUDA.
    # Set verbose=False to keep logs clean.
    reader = easyocr.Reader(['en'], gpu=False, verbose=False)
except Exception as e:
    print(f"Error: EasyOCR failed to initialize. {e}")
    reader = None

# Dataset path
dataset_dir = r"C:\Users\user\OneDrive\Desktop\farmer app\Smart-AI-Farm\dataset"

def process_image(img_path):
    """
    Checks an image for any visible text using EasyOCR and deletes it if text is found.
    """
    try:
        if not os.path.exists(img_path):
            return

        filename = os.path.basename(img_path)
        
        # Open image to check basics / close it immediately to avoid locking issues on Windows
        try:
            with Image.open(img_path) as img:
                w, h = img.size
                if w < 10 or h < 10:
                    # Too small to be a real image, might be a placeholder or corrupt
                    print(f"[REMOVED] {filename} - Too small ({w}x{h})")
                    os.remove(img_path)
                    return
        except Exception as e:
            print(f"[ERROR] Could not open {filename}: {e}")
            # If it's corrupted, maybe we should remove it anyway?
            # os.remove(img_path)
            return

        if reader is not None:
            # We use a relatively low text_threshold to catch watermarks
            # text_threshold: threshold for detecting text boxes
            # low_text: threshold for low-level text (affects sensitivity)
            results = reader.readtext(img_path, detail=1, text_threshold=0.3, low_text=0.2)
            
            # Filter results by confidence. Even low confidence text might be a watermark we want to avoid.
            valid_text_found = False
            for (bbox, text, prob) in results:
                # If we find any text with confidence > 0.15, we consider it "text content"
                if prob > 0.15:
                    valid_text_found = True
                    detected_text = text.strip()
                    break
            
            if valid_text_found:
                print(f"[REMOVED] {filename} - Text Detected: '{detected_text}' (conf: {prob:.2f})")
                
                # Close any potential handles (though with Image.open it should be fine)
                # On Windows, os.remove might fail if another process is using it.
                max_retries = 3
                for i in range(max_retries):
                    try:
                        os.remove(img_path)
                        break
                    except PermissionError:
                        time.sleep(0.5)
                return

    except Exception as e:
        print(f"[DEBUG] Error processing {img_path}: {e}")

def sweep():
    if reader is None:
        print("EasyOCR reader not available. Exiting.")
        return

    # Look for all common image formats
    extensions = ('*.png', '*.jpg', '*.jpeg', '*.webp')
    all_images = []
    
    print(f"Searching for images in {dataset_dir}...")
    
    # Recurse through all subdirectories in dataset (train, validation, etc.)
    for root, dirs, files in os.walk(dataset_dir):
        for ext in extensions:
            # We want to match files with these extensions case-insensitively
            pattern = os.path.join(root, ext)
            # glob.glob on Windows is case-insensitive for extensions usually, but let's be safe
            all_images.extend(glob.glob(pattern))
    
    if not all_images:
        print("No images found in the dataset directory.")
        return
        
    total = len(all_images)
    print(f"Found {total} images. Starting OCR-based cleaning (Aggressive Mode)...")
    
    # Use ThreadPoolExecutor to speed up (OCR is CPU intensive but can benefit from some concurrency)
    # Don't use too many workers if CPU is limited.
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_image, all_images)

if __name__ == "__main__":
    start_time = time.time()
    sweep()
    duration = time.time() - start_time
    print(f"\nCleanup finished in {duration:.2f} seconds.")
