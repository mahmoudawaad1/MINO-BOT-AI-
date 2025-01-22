import tkinter as tk
import json
from transformers import pipeline

# Initialize a pre-trained model for smarter responses (optional)
qa_pipeline = pipeline("question-answering")

# Initialize the knowledge base (data dictionary)
data = {
    "What is the meaning of 'hi'?": "Hi is a casual greeting used to say hello or to express acknowledgment of someone's presence.",
    "Hi": "Hello, how can I help you ?",
    "Hello": "Hi, how can I help you ?",
}

# Load the existing data from a file (if it exists)
def load_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return data  # Use default data if file doesn't exist

# Save the data to a file
def save_data():
    with open('data.json', 'w') as file:
        json.dump(data, file)

# Function to ask a question using predefined data
def ask_question_from_data(question):
    question = question.strip().lower()  # Clean the question for matching
    for key, value in data.items():
        if question in key.lower():
            return value
    return None

# Function to add knowledge to the AI
def add_knowledge(question, answer):
    data[question] = answer
    save_data()  # Save the new knowledge to the file
    print(f"New knowledge added: {question} -> {answer}")

# Function to handle the interaction with the AI
def ask():
    question = user_input.get()

    if question.lower() == 'quit':
        root.quit()
        return

    # First, check if the question is in the existing knowledge base
    answer = ask_question_from_data(question)
    
    if answer is None:
        # If not, ask the user to provide an answer
        conversation.config(state=tk.NORMAL)
        conversation.insert(tk.END, "I don't know the answer. Can you teach me? Please enter the answer.\n")
        conversation.config(state=tk.DISABLED)

        # Store the new question-answer pair
        add_knowledge(question, user_input.get())  # User will enter the answer
    else:
        # Otherwise, return the answer from the data
        conversation.config(state=tk.NORMAL)
        conversation.insert(tk.END, f"MINO BOT: {answer}\n")
        conversation.config(state=tk.DISABLED)

# Function to handle the conversation feedback
def feedback_yes():
    # Acknowledge helpful feedback
    conversation.config(state=tk.NORMAL)
    conversation.insert(tk.END, "MINO BOT: Thank you for the feedback! I will keep learning.\n")
    conversation.config(state=tk.DISABLED)

# Function to handle the conversation feedback when the answer is incorrect
def feedback_no():
    # Ask for the correct answer from the user
    conversation.config(state=tk.NORMAL)
    conversation.insert(tk.END, "MINO BOT: Please provide the correct answer.\n")
    conversation.config(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("MINO BOT")

# Load existing knowledge from file
data = load_data()

# Create a frame for the conversation area
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Create a text box for displaying the conversation
conversation = tk.Text(frame, height=15, width=50, wrap=tk.WORD, state=tk.DISABLED)
conversation.pack()

# Create an entry box for user input
user_input = tk.Entry(root, width=50)
user_input.pack(padx=10, pady=10)

# Create a button to submit the question
ask_button = tk.Button(root, text="Ask", command=ask)
ask_button.pack(padx=10, pady=5)

# Add a label for instructions
label = tk.Label(root, text="Type your question and click 'Ask' or type 'quit' to exit.")
label.pack(padx=10, pady=5)

# Feedback buttons (Yes and No)
feedback_yes_button = tk.Button(root, text="Yes", command=feedback_yes)
feedback_no_button = tk.Button(root, text="No", command=feedback_no)

# Run the Tkinter main loop
root.mainloop()
