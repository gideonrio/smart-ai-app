import os

# Define the structure based on user requirements
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_ROOT = os.path.join(BASE_DIR, 'dataset')

CATEGORIES = ['leaf', 'fruit', 'whole_plant', 'stem_root', 'flower', 'tuber', 'crown']
CROPS = ['tomato', 'potato', 'brinjal', 'corn', 'mango', 'banana', 'rice', 'grapes', 'citrus', 'sugarcane', 'wheat', 'onion', 'apple', 'cotton', 'groundnut', 'turmeric', 'chilli', 'coconut', 'millet']
STATUSES = ['healthy', 'affected']
SPLITS = ['train', 'validation']

def setup_structure():
    """Creates the organized dataset structure requested by the user."""
    print(f"Creating organized dataset structure in: {DATASET_ROOT}")
    
    # We follow: dataset/{split}/{category}_{crop}_{status}
    # This allows standard ImageDataGenerator to work while maintaining the requested naming
    for split in SPLITS:
        for cat in CATEGORIES:
            for crop in CROPS:
                for status in STATUSES:
                    # Creating a flat class name for standard CNN training
                    # but grouped by part and crop as requested
                    class_name = f"{cat}_{crop}_{status}"
                    path = os.path.join(DATASET_ROOT, split, class_name)
                    os.makedirs(path, exist_ok=True)
    
    print("Structure created successfully!")
    print("Please place your images in the respective folders.")
    print("Example: dataset/train/leaf_tomato_healthy/")

if __name__ == "__main__":
    setup_structure()
