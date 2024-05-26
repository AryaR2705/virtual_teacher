import os
import pytesseract
from PIL import Image

# Path to the Tesseract executable (if not in your PATH)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# List of folders containing images
folder_paths = ["student1", "student2", "student3", "student4"]

# Process each folder
for folder_path in folder_paths:
    print(f"Processing folder: {folder_path}")
    # List all files in the folder
    files = os.listdir(folder_path)
    
    # Process each image file
    for file in files:
        # Check if the file is an image
        if file.endswith((".png", ".jpg", ".jpeg", ".gif")):
            # Construct the full path to the image file
            image_path = os.path.join(folder_path, file)
            
            # Open the image file
            img = Image.open(image_path)
            
            # Use pytesseract to do OCR on the image
            text = pytesseract.image_to_string(img)
            
            # Print the extracted text
            print(f"Image: {file}\n{text}\n")
