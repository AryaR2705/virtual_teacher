import os
import pytesseract
from PIL import Image
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the CSV file
csv_path = "pratik.csv"
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
    
    return text, max(similarities) * 5

def calculate_similarity(answer, reference_answer):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([answer, reference_answer])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])
    return similarity[0][0]

# Extract reference answers from the CSV file
reference_answers = df["Answers"].tolist()

# List of folders containing images
folder_paths = ["student1", "student2", "student3", "student4"]

# Initialize a dictionary to store total marks for each folder
total_marks_per_folder = {}

# Process each image in each folder
for folder_path in folder_paths:
    total_similarity = 0
    print(f"Processing folder: {folder_path}")
    for filename in os.listdir(folder_path):
        if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
            image_path = os.path.join(folder_path, filename)
            text, max_similarity = predict_marks_from_image(image_path, reference_answers)
            total_similarity += max_similarity
            print(f"Text Extracted from {filename}:\n{text}\nMarks Obtained: {max_similarity}\n")
    total_marks_per_folder[folder_path] = total_similarity

# Print total similarity for each folder
for folder_path, total_similarity in total_marks_per_folder.items():
    print(f"Total Marks for {folder_path}: {total_similarity}")
