import openai
import streamlit as st

# Set the OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# List of interview questions
questions = [
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

# Function to evaluate answers using OpenAI API
def evaluate_answer(question, answer):
    prompt = f"Question: {question}\nAnswer: {answer}\n\nEvaluate this response on a scale of 1 to 10 and explain why."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use 'gpt-4' or any other available model
            messages=[{"role": "user", "content": prompt}],
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error evaluating answer: {e}"

# Collect responses from the user
responses = {}

for question in questions:
    user_answer = st.text_input(f"{question}")
    responses[question] = user_answer

if st.button('Evaluate Answers'):
    # Evaluate all responses
    results = []
    for question, answer in responses.items():
        evaluation = evaluate_answer(question, answer)
        results.append((question, answer, evaluation))

    # Display the results
    for result in results:
        st.write(f"**Question**: {result[0]}")
        st.write(f"**Answer**: {result[1]}")
        st.write(f"**Evaluation**: {result[2]}")
