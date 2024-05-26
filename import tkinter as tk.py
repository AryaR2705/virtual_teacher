import tkinter as tk
from tkinter import messagebox, filedialog
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create GUI window
window = tk.Tk()
window.title("Subjective Answer Script Analysis")
window.geometry("1000x1000")

# Styling the GUI window
window.configure(bg="lightgray")

# Global variables
question = ""
teacher_answer = ""

# Functions
def browse_teacher_answer():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            teacher_answer_entry.delete("1.0", tk.END)
            teacher_answer_entry.insert(tk.END, file.read())

def submit_question_answer():
    global question, teacher_answer
    question = question_entry.get("1.0", tk.END).lower()
    teacher_answer = teacher_answer_entry.get("1.0", tk.END).lower()
    messagebox.showinfo("Submission", "Question and Answer submitted successfully!")
    student_question_label.config(text="Question: " + question)

def browse_student_answer():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            student_answer_entry.delete("1.0", tk.END)
            student_answer_entry.insert(tk.END, file.read())

def submit_student_answer():
    student_answer = student_answer_entry.get("1.0", tk.END).lower()

    # Preprocess teacher and student answers
    lemmatizer = WordNetLemmatizer()
    teacher_answer_processed = ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(teacher_answer) if word not in stopwords.words('english')])
    student_answer_processed = ' '.join([lemmatizer.lemmatize(word) for word in word_tokenize(student_answer) if word not in stopwords.words('english')])

    # Compute similarity between teacher and student answers
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_features = tfidf_vectorizer.fit_transform([teacher_answer_processed, student_answer_processed])
    similarity = cosine_similarity(tfidf_features[0], tfidf_features[1])[0][0]

    # Calculate keywords and marks
    keywords = ['object', 'oops', 'encapsulation', 'Asymptotic']  # Add your keywords
    marks = 0
    for keyword in keywords:
        if keyword in student_answer_processed:
            marks += 1

    # Calculate result
    result = marks * similarity

    # Display similarity and result
    messagebox.showinfo("Result", f"Similarity between answers: {similarity:.2f}\nMarks for keywords: {marks}\nFinal result: {result:.2f}")

    # Display similarity
    messagebox.showinfo("Similarity", f"Similarity between answers: {similarity:.2f}")

 # Create label and entry for question
question_label = tk.Label(window, text="Enter Question:", bg="lightgray", font=("Arial", 14))
question_label.pack()

question_entry = tk.Text(window, width=60, height=2, font=("Arial", 12))  # Use tk.Text for multi-line text
question_entry.pack()

# Create label and entry for teacher's answer
teacher_answer_label = tk.Label(window, text="Teacher's Answer:", bg="lightgray", font=("Arial", 14))
teacher_answer_label.pack()

teacher_answer_entry = tk.Text(window, width=100, height=10, font=("Arial", 12))  # Use tk.Text for multi-line text
teacher_answer_entry.pack()

# Create button to browse teacher's answer
browse_teacher_answer_button = tk.Button(window, text="Browse", command=browse_teacher_answer, bg="blue", fg="white", font=("Arial", 12))
browse_teacher_answer_button.pack(padx=10, pady=10)

# Create submit button for question and answer
submit_button = tk.Button(window, text="Submit", command=submit_question_answer, bg="green", fg="white", font=("Arial", 12))
submit_button.pack()

# Create label for student's question
student_question_label = tk.Label(window, text="Question: ", bg="lightgray", font=("Arial", 14))
student_question_label.pack()

# Create label and entry for student's answer
student_answer_label = tk.Label(window, text="Student's Answer:", bg="lightgray", font=("Arial", 14))
student_answer_label.pack()

student_answer_entry = tk.Text(window, width=100, height=10, font=("Arial", 12))  # Use tk.Text for multi-line text
student_answer_entry.pack()

#Create button to browse student's answer
browse_student_answer_button = tk.Button(window, text="Browse", command=browse_student_answer, bg="blue", fg="white", font=("Arial", 12))
browse_student_answer_button.pack(padx=10, pady=10)

# Create submit button for student's answer
submit_student_button = tk.Button(window, text="Submit", command=submit_student_answer, bg="green", fg="white", font=("Arial", 12))
submit_student_button.pack(padx=10, pady=10)

# Run the GUI main loop
window.mainloop()