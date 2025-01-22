import tkinter as tk
import json
from transformers import pipeline

# File to store bot data
DATA_FILE = "bot_data.json"

# Initialize data and conversation history
default_data = {
    "name": "MINO BOT",
    "Why made": "To help humans in their life",
    "age": "yk i am a computer dude :/",
    "R u a human": "U want me to say yes but i am not :/",
    "can u feel ?": "Dude ur joking ??",
    "1+1": "2",
    "2+2": "4",
    "favorite color": "I like all colors equally.",
    "favorite food": "I don't eat, but I like the idea of pizza.",
    "creator": "I was created by a team of developers.",
    "purpose": "To assist and provide information.",
    "language": "I can understand and respond in multiple languages.",
    "hobbies": "I enjoy processing data and learning new things.",
    "favorite movie": "I don't watch movies, but I heard Inception is good.",
    "favorite book": "I don't read books, but I can help you find one.",
    "time": "I don't keep track of time, but your device does.",
    "weather": "I can't feel weather, but I can help you find the forecast.",
    "joke": "Why don't scientists trust atoms? Because they make up everything!",
    "quote": "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
    "fact": "Did you know? The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion."
}

# Function to load data from file
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # If file doesn't exist, return default data
        return {"data": default_data, "conversation_history": []}

# Function to save data to file
def save_data(data, conversation_history):
    with open(DATA_FILE, "w") as file:
        json.dump({"data": data, "conversation_history": conversation_history}, file)

# Load bot data
storage = load_data()
data = storage["data"]
conversation_history = storage["conversation_history"]

# Load the pre-trained model for question answering
qa_pipeline = pipeline("question-answering")

# Function to ask questions using the predefined data dictionary
def ask_question_from_data(question, data):
    for key, value in data.items():
        if question.lower() in key.lower():
            return value
    return None

# Function to ask questions using the pre-trained model
def ask_question(question, context):
    result = qa_pipeline({
        'question': question,
        'context': context
    })
    return result['answer']

# Example context for model-based answering
context = """
Artificial intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions. The term may also be applied to any machine that exhibits traits associated with a human mind such as learning and problem-solving. As machines become increasingly capable, tasks once thought to require human intelligence are now being performed by AI systems.
"""

# Function to handle the interaction with improved memory and learning
def ask():
    global current_question  # Make sure we can use this variable in the whole function

    question = user_input.get()

    if question.lower() == 'quit':
        root.quit()
        return

    # Check if the question is already in the data (previously learned responses)
    answer = ask_question_from_data(question, data)

    # If the question is not found in predefined data, use the model to generate an answer
    if answer is None:
        answer = ask_question(question, context)

    # Add the conversation to history to make the bot aware of past interactions
    conversation_history.append(f"You: {question}")
    conversation_history.append(f"MINO BOT: {answer}")

    # Save updated conversation history
    save_data(data, conversation_history)

    # Update the conversation window
    conversation.config(state=tk.NORMAL)  # Make the Text widget editable
    conversation.delete(1.0, tk.END)  # Clear the previous conversation
    conversation.insert(tk.END, "\n".join(conversation_history) + "\n")
    conversation.config(state=tk.DISABLED)  # Make the Text widget non-editable again

    # Store the current question
    current_question = question

# Function to handle feedback when user answers "no"
def feedback_no():
    conversation_history.append("MINO BOT: Please provide the correct answer.")
    conversation.config(state=tk.NORMAL)
    conversation.insert(tk.END, "MINO BOT: Please provide the correct answer.\n")
    conversation.config(state=tk.DISABLED)
    user_input.delete(0, tk.END)

# Function to submit the corrected answer
def submit_correct_answer():
    corrected_answer = user_input.get()
    if corrected_answer.strip() != "":
        data[current_question] = corrected_answer  # Update the answer in the data
        save_data(data, conversation_history)  # Save updated data

# Create the main window
root = tk.Tk()
root.title("MINO BOT")

# Create a frame for the conversation area
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Create a text box for displaying the conversation
conversation = tk.Text(frame, height=15, width=50, wrap=tk.WORD, state=tk.DISABLED)
conversation.pack()

# Restore previous conversation
conversation.config(state=tk.NORMAL)
conversation.insert(tk.END, "\n".join(conversation_history) + "\n")
conversation.config(state=tk.DISABLED)

# Create an entry box for user input
user_input = tk.Entry(root, width=50)
user_input.pack(padx=10, pady=10)

# Create a button to submit the question
ask_button = tk.Button(root, text="Ask", command=ask)
ask_button.pack(padx=10, pady=5)

# Run the Tkinter main loop
root.mainloop()
#The end :D
