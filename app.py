import openai
import streamlit as st

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# List of 10 predefined questions
questions_list = [
    "Tell me about yourself.",
    "Why do you want to work with us?",
    "What is your greatest strength?",
    "What is your biggest weakness?",
    "Describe a challenging situation you faced and how you overcame it.",
    "How do you prioritize tasks when working on multiple projects?",
    "What do you know about our company?",
    "Where do you see yourself in 5 years?",
    "Why should we hire you?",
    "What are your salary expectations?"
]

# Function to evaluate the answer
def evaluate_answer(question, answer):
    prompt = f"Question: {question}\nAnswer: {answer}\n\nEvaluate this response on a scale of 1 to 10 and explain why."
    try:
        # Using the new OpenAI API
        response = openai.Completion.create(
            model="text-davinci-003",  # Or another model (e.g., text-ada-001, etc.)
            prompt=prompt,
            max_tokens=100,  # Adjust max tokens if necessary
            temperature=0.7  # Adjust temperature for response randomness
        )
        # Return the evaluation result
        return response.choices[0].text.strip()
    except Exception as e:
        # Return any errors encountered
        return f"Error evaluating answer: {e}"

# Streamlit UI components
st.title("Interview Question Evaluator")

# Select a question from the predefined list
question = st.selectbox("Choose a question", questions_list)

# Input field for answer
answer = st.text_area("Enter your answer:")

# Button to evaluate the answer
if st.button("Evaluate Answer"):
    if answer:
        evaluation = evaluate_answer(question, answer)
        st.write("Evaluation:")
        st.write(evaluation)
    else:
        st.write("Please enter an answer.")
