import os
import pytesseract
from PIL import Image
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the CSV file
csv_path = "dataset.csv"
df = pd.read_csv(csv_path)

# Define a function to predict marks for a given answer
def predict_marks_from_image(image_path, reference_answers):
    # Open the image file
    img = Image.open(image_path)
    
    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(img)
    
    # Calculate cosine similarity with each reference answer
    similarities = []
    for reference_answer in reference_answers:
        similarity = calculate_similarity(text, reference_answer)
        similarities.append(similarity)
    
    return similarities

def calculate_similarity(answer, reference_answer):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([answer, reference_answer])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return similarity[0][0]

# Extract reference answers from the CSV file
reference_answers = df["Answers"].tolist()

# Folder containing images
folder_path = "images_folder"

# Initialize a dictionary to store max similarities for each image
max_similarities = {}

# Process each image in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_path = os.path.join(folder_path, filename)
        similarities = predict_marks_from_image(image_path, reference_answers)
        max_similarity = max(similarities) * 5  # Multiply by 5 to match your scaling
        max_similarities[filename] = max_similarity

# Print max similarities for each image
for filename, max_similarity in max_similarities.items():
    print(f"Max Similarity for {filename}: {max_similarity}")
