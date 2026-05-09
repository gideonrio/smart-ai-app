import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from bing_image_downloader import downloader

dataset_dir = r"C:\Users\user\OneDrive\Desktop\farmer app\Smart-AI-Farm\dataset\train"
temp_dir = r"C:\Users\user\OneDrive\Desktop\farmer app\Smart-AI-Farm\temp_images"

if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

def download_for_folder(folder):
    parts = folder.split('_')
    # Improve query: e.g., 'crown_apple_healthy' -> 'crown apple healthy agricultural photo'
    # adding terms to ensure rural/plant imagery
    query = " ".join(parts) + " real agriculture plant leaf fruit"
    target_folder = os.path.join(dataset_dir, folder)
    
    try:
        # Check if already has enough images
        existing_files = [f for f in os.listdir(target_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if len(existing_files) >= 50:
            return f"{folder} already has {len(existing_files)} images. Skipping."

        # Download up to 50 images per category
        limit = 50 - len(existing_files)
        if limit <= 0:
            return f"{folder} already has enough."

        # Download will create a subfolder temp_images/query
        downloader.download(query, limit=limit, output_dir=temp_dir, adult_filter_off=True, force_replace=False, timeout=60, verbose=False)
        downloaded_folder = os.path.join(temp_dir, query)
        
        count = 0
        if os.path.exists(downloaded_folder):
            for file_name in os.listdir(downloaded_folder):
                src = os.path.join(downloaded_folder, file_name)
                
                # Make a unique destination name
                base, ext = os.path.splitext(file_name)
                dst = os.path.join(target_folder, f"real_img_{count}{ext}")
                
                while os.path.exists(dst):
                    count += 1
                    dst = os.path.join(target_folder, f"real_img_{count}{ext}")
                    
                shutil.move(src, dst)
                count += 1
                if count >= limit:
                    break
            shutil.rmtree(downloaded_folder)
        return f"Success for {folder}: downloaded {count} new real images."
    except Exception as e:
        return f"Failed for {folder}: {str(e)}"

if __name__ == "__main__":
    folders = [f for f in os.listdir(dataset_dir) if os.path.isdir(os.path.join(dataset_dir, f))]
    print(f"Starting concurrent download of REAL images for {len(folders)} classes...")
    
    # Using thread pool to speed up the thousands of downloads
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(download_for_folder, folder): folder for folder in folders}
        for future in as_completed(futures):
            print(future.result())

    print("SUCCESS: Finished downloading real dataset images.")
