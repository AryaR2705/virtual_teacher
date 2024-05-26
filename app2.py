import pytesseract
from PIL import Image

# Path to the Tesseract executable (replace with your path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Path to your handwritten image
image_path = 'img.png'

# Open the image file
img = Image.open(image_path)

# Use pytesseract to extract text
text = pytesseract.image_to_string(img)

# Print the extracted text
print(text)
