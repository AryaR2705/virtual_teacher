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
reference_answers = df["title"].tolist()

# List of image paths
image_paths = ['img2.png', 'img13.png']

# Process each image
for image_path in image_paths:
    similarities = predict_marks_from_image(image_path, reference_answers)
    for i, similarity in enumerate(similarities):
        print(f"Image: {image_path}, Title: {df.loc[i, 'title']}, Similarity: {similarity}\n")
